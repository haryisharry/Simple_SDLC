#!/usr/bin/env python3
"""Local SimpleSDLC scaffolding and structural checks. No network or model calls."""

from __future__ import annotations

import argparse
import heapq
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path, PureWindowsPath
import re
import shutil
import stat
import sys
import tarfile
import time
import uuid
import zipfile


TASK_ID = re.compile(r"TASK-\d{3,}\Z")
HANDOFF_ID = re.compile(r"HANDOFF-\d{3,}\Z")
STATUSES = {
    "NONE", "DRAFT", "READY", "IN_PROGRESS", "SUBMITTED",
    "CHANGES_REQUESTED", "BLOCKED", "ACCEPTED",
}
STAGES = {
    "discovery", "requirements", "design", "planning", "implementation",
    "verification", "uat", "release", "maintenance",
}
ROLES = {"manager", "worker", "human"}
DIRECTORIES = (
    "requirements", "design", "tasks", "reports", "reviews", "testing",
    "evidence", "handoffs/history",
)
DOCUMENTS = {
    "brief.md": "brief.md",
    "discovery.md": "discovery.md",
    "decisions.md": "decisions.md",
    "traceability.md": "traceability.md",
    "implementation-plan.md": "implementation-plan.md",
    "test-plan.md": "testing/plan.md",
    "uat.md": "testing/uat.md",
    "task-matrix.json": "task-matrix.json",
}

MATRIX_STORE = {"schema_version": 2, "storage": "task-matrices"}
ROOT_BYTES, ROOT_LINES = 8192, 120
RECORD_BYTES, RECORD_LINES = 49152, 600
PAGE_BYTES = 12000


def project_path(project: Path, relative: str) -> Path:
    """Resolve a project-relative record without links or escaping the project."""
    info = project.lstat()
    if project.is_symlink() or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
        raise ValueError("Linked project records are not supported.")
    raw = Path(relative.replace("\\", "/"))
    if raw.is_absolute() or PureWindowsPath(relative).drive or ".." in raw.parts:
        raise ValueError("Record path must stay inside project records.")
    current = project
    for part in raw.parts:
        current = current / part
        info = current.lstat()
        if current.is_symlink() or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            raise ValueError("Linked project records are not supported.")
    if project.resolve() not in current.resolve().parents:
        raise ValueError("Record path must name a file inside project records.")
    return current


def load_task_matrix(project: Path) -> dict:
    """Full machine audit only. Agents should open one shard, never this combined view."""
    manifest = read_json(project / "task-matrix.json")
    if manifest.get("schema_version") == 1 and isinstance(manifest.get("tasks"), list):
        return manifest
    if manifest != MATRIX_STORE:
        raise ValueError("Task matrix requires schema_version 1 with tasks, or the schema_version 2 storage descriptor.")
    directory = project_path(project, "task-matrices")
    if not directory.is_dir():
        raise ValueError("Missing task-matrices directory.")
    tasks = []
    for path in sorted(directory.iterdir()):
        if path.name == "legacy-v1.json":
            continue
        if path.suffix != ".json" or not TASK_ID.fullmatch(path.stem):
            raise ValueError(f"Unexpected matrix shard: {path.name}")
        task = read_json(project_path(project, f"task-matrices/{path.name}"))
        if task.get("id") != path.stem:
            raise ValueError(f"Matrix shard filename/ID mismatch: {path.name}")
        tasks.append(task)
    return {"schema_version": 1, "tasks": tasks}


def migrate_matrix(project: Path) -> str:
    """Lossless v1 -> v2 migration; descriptor replacement is the commit point."""
    source = project_path(project, "task-matrix.json")
    original = source.read_bytes()
    manifest = read_json(source)
    if manifest == MATRIX_STORE:
        load_task_matrix(project)
        return "Matrix already uses per-task storage; nothing changed."
    if set(manifest) != {"schema_version", "tasks"} or manifest.get("schema_version") != 1 or not isinstance(manifest.get("tasks"), list):
        raise ValueError("Migration requires a v1 matrix with only schema_version and tasks; reconcile unknown fields first.")
    ids = [task.get("id") if isinstance(task, dict) else None for task in manifest["tasks"]]
    if any(not isinstance(item, str) or not TASK_ID.fullmatch(item) for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("Migration refuses invalid or duplicate task IDs.")
    target = project / "task-matrices"
    # A previous interruption may have published the store but not the descriptor.
    if target.exists() or target.is_symlink():
        project_path(project, "task-matrices")
        expected = {f"{item}.json" for item in ids} | {"legacy-v1.json"}
        if {path.name for path in target.iterdir()} != expected:
            raise ValueError("Existing task-matrices does not match a recoverable migration; preserve and reconcile it.")
        if project_path(project, "task-matrices/legacy-v1.json").read_bytes() != original:
            raise ValueError("Migration backup differs from the current matrix; refusing overwrite.")
        for task in manifest["tasks"]:
            if read_json(project_path(project, f"task-matrices/{task['id']}.json")) != task:
                raise ValueError("Existing migration shard differs; refusing overwrite.")
    else:
        with staging_directory(project.parent, ".matrix-") as temporary:
            staged = temporary / "task-matrices"
            staged.mkdir()
            (staged / "legacy-v1.json").write_bytes(original)
            for task in manifest["tasks"]:
                write_json(staged / f"{task['id']}.json", task)
            publish_staged(staged, target)
    with staging_directory(project.parent, ".matrix-") as temporary:
        descriptor = temporary / "task-matrix.json"
        write_json(descriptor, MATRIX_STORE)
        if source.read_bytes() != original:
            raise ValueError("Matrix changed during migration; refusing descriptor replacement.")
        os.replace(descriptor, source)
    return f"Migrated {len(ids)} tasks; exact original retained in task-matrices/legacy-v1.json. Run check."


def memory_issues(project: Path) -> list[str]:
    """Check all working records, including unknown/custom formats; history stays cold."""
    errors = []
    for path in project.rglob("*"):
        info = path.lstat()
        if path.is_symlink() or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            errors.append(f"Linked project records are not supported: {path.relative_to(project)}")
            continue
        if not path.is_file():
            continue
        relative = path.relative_to(project)
        parts = relative.parts
        cold = parts[0] in {"evidence", "history", "contracts"} or parts[:2] == ("handoffs", "history") or relative.as_posix() == "task-matrices/legacy-v1.json"
        if cold:
            continue
        root = len(parts) == 1 or relative.as_posix() == "handoffs/current.md"
        byte_limit, line_limit = (ROOT_BYTES, ROOT_LINES) if root else (RECORD_BYTES, RECORD_LINES)
        size = path.stat().st_size
        # Do not load a huge/custom/binary working record just to count its lines.
        if size > byte_limit:
            errors.append(f"Memory budget exceeded: {relative.as_posix()} ({size} bytes > {byte_limit}); partition before handoff.")
        else:
            data = path.read_bytes()
            lines = len(data.splitlines())
            if lines > line_limit:
                errors.append(f"Memory budget exceeded: {relative.as_posix()} ({lines} lines > {line_limit}); partition before handoff.")
    return errors


def read_record(project: Path, relative: str, offset: int = 0, limit: int = PAGE_BYTES) -> dict:
    if offset < 0 or not 1 <= limit <= PAGE_BYTES:
        raise ValueError(f"Use offset >= 0 and limit 1..{PAGE_BYTES} bytes.")
    path = project_path(project, relative)
    with path.open("rb") as stream:
        stream.seek(offset)
        data = stream.read(limit)
    # Byte offsets are exact; split UTF-8 characters render as replacement characters.
    return {"path": relative, "offset": offset, "next_offset": offset + len(data),
            "more": offset + len(data) < path.stat().st_size, "text": data.decode("utf-8", errors="replace")}


def task_page(project: Path, after: str = "", limit: int = 20) -> dict:
    if not 1 <= limit <= 50 or (after and not TASK_ID.fullmatch(after)):
        raise ValueError("Use a TASK-NNN cursor and limit 1..50.")
    paths = heapq.nsmallest(limit + 1, (p for p in (project / "tasks").glob("TASK-*.md") if TASK_ID.fullmatch(p.stem) and p.stem > after), key=lambda p: p.stem)
    return {"tasks": [p.stem for p in paths[:limit]], "after": paths[limit - 1].stem if len(paths) > limit else None}


def context_routes(project: Path) -> dict:
    for relative in ("state.json", "task-matrix.json", "handoffs/current.md"):
        path = project_path(project, relative)
        # The v1 matrix is only checked for size here, never loaded into agent context.
        if path.stat().st_size > ROOT_BYTES:
            raise ValueError(f"{relative} exceeds the startup budget; use migrate-matrix or paged read-record.")
    state = read_json(project / "state.json")
    task = state.get("active_task")
    if task is not None and (not isinstance(task, str) or not TASK_ID.fullmatch(task)):
        raise ValueError("Invalid active task.")
    manifest = read_json(project / "task-matrix.json")
    routes = ["state.json", "handoffs/current.md"]
    if task:
        routes += [f"tasks/{task}.md"]
        if manifest == MATRIX_STORE:
            routes += [f"task-matrices/{task}.json"]
        else:
            raise ValueError("Migrate the legacy matrix before loading active task context.")
    else:
        routes += ["brief.md", "discovery.md", "implementation-plan.md"]
    return {"active_role": state.get("active_role"), "active_task": task,
            "read_next": routes, "instruction": "Use read-record pages and task-specific links. Do not read all history or indexes."}


@contextmanager
def staging_directory(parent: Path, prefix: str):
    """Use inherited workspace permissions, including in restricted Windows sessions."""
    parent = parent.resolve()
    directory = parent / f"{prefix}{uuid.uuid4().hex}"
    directory.mkdir()
    try:
        yield directory
    finally:
        # Only remove the uniquely created staging directory under the known parent.
        if directory.is_symlink() or directory.resolve().parent != parent:
            raise ValueError("Staging directory identity changed; refusing cleanup.")
        if directory.exists():
            shutil.rmtree(directory)


def publish_staged(source: Path, destination: Path) -> None:
    """Retry transient Windows rename failures without replacing existing records."""
    for attempt in range(4):
        if destination.exists() or destination.is_symlink():
            raise ValueError("Destination appeared during staging; nothing will be overwritten.")
        try:
            source.rename(destination)
            return
        except PermissionError as exc:
            if getattr(exc, "winerror", None) not in (5, 32, 33) or attempt == 3:
                raise
            time.sleep(0.1 * (2 ** attempt))


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def metadata(path: Path) -> dict[str, str]:
    """Read only the leading metadata block; document body is not metadata."""
    result = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            break
        key, separator, value = line.partition(":")
        if not separator or key.strip() in result:
            raise ValueError(f"Invalid or duplicate metadata in {path.name}")
        result[key.strip()] = value.strip()
    return result


def initialize(ai_root: Path, name: str, mode: str) -> Path:
    ai_root = ai_root.resolve()
    if not name.strip():
        raise ValueError("Project name must not be blank.")
    if mode not in {"greenfield", "brownfield"}:
        raise ValueError("Mode must be greenfield or brownfield.")
    project = ai_root / "project"
    if project.exists() or project.is_symlink():
        raise ValueError("Project records already exist; initialization will not overwrite them.")
    templates = ai_root / "framework" / "templates"
    config = read_json(templates / "config.json")
    config.update({
        "project_name": name.strip(),
        "project_id": str(uuid.uuid4()),
        "project_root": str(ai_root.parent),
        "mode": mode,
        "framework_version": (ai_root / "framework" / "VERSION").read_text().strip(),
    })
    state = read_json(templates / "state.json")
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    # A failed setup leaves no half-initialized project directory.
    with staging_directory(ai_root, ".init-") as temporary:
        staged = Path(temporary) / "project"
        staged.mkdir()
        for directory in DIRECTORIES:
            (staged / directory).mkdir(parents=True, exist_ok=True)
        for source, destination in DOCUMENTS.items():
            shutil.copyfile(templates / source, staged / destination)
        (staged / "task-matrices").mkdir()
        write_json(staged / "config.json", config)
        write_json(staged / "state.json", state)
        (staged / "handoffs" / "current.md").write_text(
            "ID: HANDOFF-000\nTo: manager\nTask: none\nContract: none\n\n"
            "# Initial manager handoff\n\n"
            "Follow `.ai/START_MANAGER.md` and `.ai/framework/BOOTSTRAP.md`.\n"
            "Inspect this project and clarify its business needs before issuing work.\n"
            "Initial documents are drafts; no implementation or acceptance has occurred.\n",
            encoding="utf-8",
        )
        publish_staged(staged, project)
    return project


def check_task_matrix(project: Path, state: dict, ready: bool) -> list[str]:
    """Validate task contracts and evidence references, never infer a test result."""
    errors: list[str] = []
    try:
        matrix = load_task_matrix(project)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    if matrix.get("schema_version") != 1 or not isinstance(matrix.get("tasks"), list):
        return ["Task matrix requires schema_version 1 and a tasks list."]
    tasks: dict[str, dict] = {}
    statuses: dict[str, str] = {}

    def meaningful(value) -> bool:
        return isinstance(value, str) and bool(value.strip()) and "TODO" not in value and not value.startswith("SET_")

    for task in matrix["tasks"]:
        task_id = task.get("id") if isinstance(task, dict) else None
        if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
            errors.append("Matrix has an invalid task ID.")
            continue
        if task_id in tasks:
            errors.append(f"Duplicate matrix task: {task_id}")
            continue
        tasks[task_id] = task
        try:
            task_meta = metadata(project / "tasks" / f"{task_id}.md")
            statuses[task_id] = task_meta.get("Status", "")
            if task_meta.get("ID") != task_id or statuses[task_id] not in STATUSES - {"NONE"}:
                errors.append(f"{task_id}: invalid task document metadata.")
            if type(task.get("revision")) is not int or task["revision"] < 1:
                errors.append(f"{task_id}: revision must be a positive integer.")
            elif task_meta.get("Contract") != str(task["revision"]):
                errors.append(f"{task_id}: task Contract disagrees with matrix revision.")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
        status = statuses.get(task_id)
        prepared = status not in (None, "DRAFT")
        accepted = status == "ACCEPTED"
        if task.get("scope_review") not in ("DRAFT", "READY"):
            errors.append(f"{task_id}: scope_review must be DRAFT or READY.")
        if prepared and task.get("scope_review") != "READY":
            errors.append(f"{task_id}: manager scope review must be READY before execution/closure.")
        if prepared and (not meaningful(task.get("feature")) or not meaningful(task.get("inventory_note"))):
            errors.append(f"{task_id}: parent feature and manager inventory note are required.")
        dependencies = task.get("depends_on")
        if not isinstance(dependencies, list) or any(not isinstance(item, str) or not TASK_ID.fullmatch(item) for item in dependencies):
            errors.append(f"{task_id}: depends_on must contain valid task IDs.")
        elif len(set(dependencies)) != len(dependencies):
            errors.append(f"{task_id}: duplicate dependencies.")
        touchpoints = task.get("touchpoints")
        checks = task.get("checks")
        if not isinstance(touchpoints, list) or not isinstance(checks, list):
            errors.append(f"{task_id}: touchpoints and checks must be lists.")
            continue
        if prepared and (not touchpoints or not checks):
            errors.append(f"{task_id}: execution requires touchpoints and observable checks.")
        point_ids: set[str] = set()
        for point in touchpoints:
            point_id = point.get("id") if isinstance(point, dict) else None
            if not meaningful(point_id) or point_id in point_ids:
                errors.append(f"{task_id}: invalid/duplicate touchpoint ID.")
                continue
            point_ids.add(point_id)
            if point.get("action") not in ("CHANGE", "VERIFY_UNCHANGED"):
                errors.append(f"{task_id}/{point_id}: invalid touchpoint action.")
            if prepared and any(not meaningful(point.get(field)) for field in ("path", "surface", "reason")):
                errors.append(f"{task_id}/{point_id}: path, surface and reason are required.")
        covered: set[str] = set()
        check_ids: set[str] = set()
        for item in checks:
            check_id = item.get("id") if isinstance(item, dict) else None
            if not meaningful(check_id) or check_id in check_ids:
                errors.append(f"{task_id}: invalid/duplicate check ID.")
                continue
            check_ids.add(check_id)
            label = f"{task_id}/{check_id}"
            references = item.get("touchpoints")
            if not isinstance(references, list) or not references or any(not isinstance(ref, str) or ref not in point_ids for ref in references):
                errors.append(f"{label}: check must reference existing touchpoints.")
            else:
                covered.update(references)
            if item.get("mode") not in ("AUTOMATED", "BROWSER", "MANUAL", "ENVIRONMENT", "HUMAN"):
                errors.append(f"{label}: invalid verification mode.")
            if prepared and any(not meaningful(item.get(field)) for field in ("criterion", "scenario", "method", "expected")):
                errors.append(f"{label}: criterion, scenario, method and expected observation are required.")
            result = item.get("result")
            if not isinstance(result, dict) or result.get("status") not in ("NOT_RUN", "PASS", "FAIL", "BLOCKED", "NOT_APPLICABLE"):
                errors.append(f"{label}: invalid result record.")
                continue
            if item.get("review") not in ("PENDING", "ACCEPTED", "CHANGES_REQUESTED"):
                errors.append(f"{label}: invalid manager review status.")
            evidence = result.get("evidence")
            if not isinstance(evidence, list):
                errors.append(f"{label}: evidence must be a list.")
                evidence = []
            for artifact in evidence:
                path = artifact.get("path") if isinstance(artifact, dict) else None
                if not meaningful(path) or not meaningful(artifact.get("locator")):
                    errors.append(f"{label}: evidence needs a path and exact locator.")
                    continue
                relative = Path(path.replace("\\", "/"))
                resolved = (project / relative).resolve()
                if relative.is_absolute() or PureWindowsPath(path).drive or project.resolve() not in resolved.parents or any(char in path for char in "*?[]"):
                    errors.append(f"{label}: evidence path must be concrete and inside project records.")
                    continue
                if not resolved.is_file() or resolved.stat().st_size == 0:
                    errors.append(f"{label}: missing or empty evidence: {path}")
            if result["status"] == "PASS" and (not evidence or not meaningful(result.get("code_identity"))):
                errors.append(f"{label}: PASS requires evidence and code identity.")
            if (result["status"] == "PASS" or item.get("review") == "ACCEPTED") and result.get("contract_revision") != task.get("revision"):
                errors.append(f"{label}: result contract revision is stale or missing.")
            if result["status"] in ("BLOCKED", "NOT_APPLICABLE") and not meaningful(result.get("reason")):
                errors.append(f"{label}: blocked/not-applicable result requires a reason.")
            if accepted:
                if item.get("review") != "ACCEPTED" or result["status"] not in ("PASS", "NOT_APPLICABLE"):
                    errors.append(f"{label}: task acceptance requires manager-accepted passing checks or justified exclusions.")
                if result["status"] == "PASS" and result.get("code_identity") != task.get("reviewed_code_identity"):
                    errors.append(f"{label}: evidence code identity differs from manager-reviewed snapshot.")
        if prepared:
            for point_id in sorted(point_ids - covered):
                errors.append(f"{task_id}/{point_id}: uncovered touchpoint; add an observable check.")
        if accepted and not meaningful(task.get("reviewed_code_identity")):
            errors.append(f"{task_id}: accepted task requires reviewed_code_identity.")

    for path in (project / "tasks").glob("TASK-*.md"):
        if path.stem not in tasks:
            errors.append(f"Task document missing from matrix: {path.stem}")
    for task_id, task in tasks.items():
        dependencies = task.get("depends_on")
        if not isinstance(dependencies, list):
            continue
        for dependency in dependencies:
            if not isinstance(dependency, str):
                continue
            if dependency not in tasks:
                errors.append(f"{task_id}: unknown dependency {dependency}.")
            elif (statuses.get(task_id) == "ACCEPTED" or (ready and task_id == state.get("active_task") and state.get("active_role") == "worker")) and statuses.get(dependency) != "ACCEPTED":
                errors.append(f"{task_id}: dependency {dependency} is not ACCEPTED.")
    visiting: set[str] = set()
    visited: set[str] = set()

    for task_id in tasks:
        stack = [(task_id, False)]
        while stack:
            current, leaving = stack.pop()
            if leaving:
                visiting.discard(current)
                visited.add(current)
            elif current in visiting:
                errors.append(f"Dependency cycle includes {current}.")
            elif current not in visited:
                visiting.add(current)
                stack.append((current, True))
                dependencies = tasks[current].get("depends_on", [])
                if isinstance(dependencies, list):
                    stack.extend((dependency, False) for dependency in dependencies if isinstance(dependency, str) and dependency in tasks)
    active = state.get("active_task")
    if isinstance(active, str) and active not in tasks:
        errors.append("Active task has no task-matrix contract.")
    try:
        handoff = metadata(project / "handoffs" / "current.md")
        revision = str(tasks[active].get("revision")) if isinstance(active, str) and active in tasks else "none"
        if handoff.get("Contract") != revision:
            errors.append("Current handoff Contract disagrees with task-matrix revision.")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def check(ai_root: Path, ready: bool = False) -> list[str]:
    ai_root = ai_root.resolve()
    project = ai_root / "project"
    errors: list[str] = []
    if not project.is_dir() or project.is_symlink():
        return ["No ordinary project directory. Initialize this project before use."]
    # Reject linked state so validation cannot accidentally read another project.
    for entry in project.rglob("*"):
        if entry.is_symlink() or getattr(entry.lstat(), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            errors.append(f"Project records must not be symbolic links: {entry.relative_to(project)}")
    if errors:
        return errors
    errors.extend(memory_issues(project))
    if errors:
        return errors
    for directory in DIRECTORIES:
        if not (project / directory).is_dir():
            errors.append(f"Missing directory: project/{directory}")
    for document in DOCUMENTS.values():
        if not (project / document).is_file():
            errors.append(f"Missing document: project/{document}")
    try:
        config = read_json(project / "config.json")
        state = read_json(project / "state.json")
    except (OSError, ValueError) as exc:
        return errors + [str(exc)]
    if config.get("schema_version") != 1 or state.get("schema_version") != 1:
        errors.append("Unsupported schema_version; review migration before continuing.")
    expected_version = (ai_root / "framework" / "VERSION").read_text().strip()
    if config.get("framework_version") != expected_version:
        errors.append("Project/framework version mismatch; review the framework upgrade.")
    try:
        uuid.UUID(config.get("project_id", ""))
    except (ValueError, AttributeError, TypeError):
        errors.append("project_id must be a UUID.")
    if not isinstance(config.get("project_name"), str) or not config["project_name"].strip():
        errors.append("project_name must be nonempty.")
    configured_root = config.get("project_root")
    if not isinstance(configured_root, str) or not Path(configured_root).is_absolute():
        errors.append("project_root must be an absolute path.")
    elif Path(configured_root).resolve() != ai_root.parent:
        errors.append("Project root mismatch: use a clean export for a new project; review identity before rebinding a moved project.")
    if config.get("mode") not in {"greenfield", "brownfield"}:
        errors.append("Invalid project mode.")
    if config.get("dispatch") != "manual" or config.get("single_writer") is not True:
        errors.append("Version 1 requires manual dispatch and single_writer: true.")
    if config.get("manager_write_scope") != ".ai":
        errors.append("Version 1 requires manager_write_scope: .ai.")
    roles = config.get("roles")
    for role in ("manager", "worker"):
        assignment = roles.get(role) if isinstance(roles, dict) else None
        if not isinstance(assignment, dict) or any(
            not isinstance(assignment.get(field), str) or not assignment[field].strip()
            for field in ("model", "application")
        ):
            errors.append(f"Configure model and application labels for {role}.")
    actor = state.get("active_role")
    status = state.get("task_status")
    task_id = state.get("active_task")
    if not isinstance(actor, str) or actor not in ROLES:
        errors.append("Invalid active_role.")
    if not isinstance(status, str) or status not in STATUSES:
        errors.append("Invalid task_status.")
    if not isinstance(state.get("stage"), str) or state["stage"] not in STAGES:
        errors.append("Invalid lifecycle stage.")
    if not isinstance(state.get("summary"), str) or not state["summary"].strip():
        errors.append("State summary must be nonempty.")
    try:
        timestamp = datetime.fromisoformat(state.get("updated_at", "").replace("Z", "+00:00"))
        if timestamp.utcoffset() is None or timestamp.utcoffset().total_seconds() != 0:
            raise ValueError("Timestamp must use UTC.")
    except (ValueError, TypeError, AttributeError):
        errors.append("updated_at must be an ISO 8601 UTC timestamp.")
    if task_id is None:
        if status != "NONE" or actor == "worker":
            errors.append("No active task requires task_status NONE and manager/human ownership.")
    elif not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
        errors.append("Invalid active_task; use TASK-001 style IDs.")
    else:
        task_path = project / "tasks" / f"{task_id}.md"
        try:
            task_meta = metadata(task_path)
            if task_meta.get("ID") != task_id or task_meta.get("Status") != status:
                errors.append("Active task metadata disagrees with state.")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
        if status == "NONE":
            errors.append("An active task cannot have status NONE.")
        if status in {"SUBMITTED", "ACCEPTED"} and not any((project / "reports").glob(f"{task_id}-attempt-*.md")):
            errors.append("Submitted/accepted task requires a worker report.")
        if status in {"CHANGES_REQUESTED", "ACCEPTED"} and not any((project / "reviews").glob(f"{task_id}-attempt-*.md")):
            errors.append("Changes-requested/accepted task requires a manager review.")
    if actor == "worker" and status not in {"READY", "IN_PROGRESS", "CHANGES_REQUESTED"}:
        errors.append("Worker ownership requires READY, IN_PROGRESS, or CHANGES_REQUESTED.")
    if status == "IN_PROGRESS" and actor != "worker":
        errors.append("IN_PROGRESS requires worker ownership; record a blocker before returning control.")
    if state.get("current_handoff") != "handoffs/current.md":
        errors.append("current_handoff must be handoffs/current.md.")
    else:
        handoff_path = project / "handoffs" / "current.md"
        try:
            handoff = metadata(handoff_path)
            if not HANDOFF_ID.fullmatch(handoff.get("ID", "")):
                errors.append("Current handoff needs a HANDOFF-001 style ID.")
            if handoff.get("To") != actor:
                errors.append("Current handoff recipient disagrees with active_role.")
            if handoff.get("Task") != (task_id or "none"):
                errors.append("Current handoff task disagrees with active_task.")
            if ready and "TODO" in handoff_path.read_text(encoding="utf-8-sig"):
                errors.append("Current handoff still contains TODO placeholders.")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    if ready and actor == "worker" and isinstance(task_id, str) and TASK_ID.fullmatch(task_id):
        task_path = project / "tasks" / f"{task_id}.md"
        if task_path.is_file() and "TODO" in task_path.read_text(encoding="utf-8-sig"):
            errors.append("Worker task still contains TODO placeholders.")
    errors.extend(check_task_matrix(project, state, ready))
    return errors


def export_clean(ai_root: Path, destination: Path) -> Path:
    ai_root = ai_root.resolve()
    # Check the supplied path before resolve() to reject dangling links too.
    if destination.exists() or destination.is_symlink():
        raise ValueError("Export destination already exists; nothing will be overwritten.")
    destination = destination.resolve()
    if destination.name != ".ai":
        raise ValueError("Export destination must be a new folder named .ai.")
    if destination == ai_root or ai_root in destination.parents:
        raise ValueError("Export destination cannot be inside the source .ai folder.")

    def ignored(directory: str, names: list[str]) -> set[str]:
        exclusions = {name for name in names if name in {"__pycache__", ".git"} or name.endswith(".pyc") or name.startswith((".init-", ".export-"))}
        if Path(directory).resolve() == ai_root:
            exclusions.add("project")
        for name in set(names) - exclusions:
            if (Path(directory) / name).is_symlink():
                raise ValueError("Clean export refuses symbolic links in framework files.")
        return exclusions

    destination.parent.mkdir(parents=True, exist_ok=True)
    with staging_directory(destination.parent, ".export-") as temporary:
        staged = Path(temporary) / ".ai"
        shutil.copytree(ai_root, staged, ignore=ignored)
        publish_staged(staged, destination)
    return destination


def check_delivery(artifact: Path) -> list[str]:
    """Inspect names/types only; do not extract, follow links or inspect nested archives."""
    errors: list[str] = []
    files = 0

    def inspect_name(name: str) -> None:
        parts = name.replace("\\", "/").split("/")
        if any(part.casefold() == ".ai" for part in parts):
            errors.append(f"Delivery contains .ai: {name}")
        if ".." in parts or name.startswith(("/", "\\")) or PureWindowsPath(name).drive:
            errors.append(f"Unsafe artifact member path: {name}")

    def linked(path: Path) -> bool:
        info = path.lstat()
        return stat.S_ISLNK(info.st_mode) or (stat.S_ISREG(info.st_mode) and info.st_nlink > 1) or bool(
            getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        )

    def walk_error(error: OSError) -> None:
        raise error

    try:
        if linked(artifact):
            return ["Delivery artifact must not be a link or reparse point."]
        inspect_name(artifact.name)
        if artifact.is_dir():
            for directory, dirs, names in os.walk(artifact, followlinks=False, onerror=walk_error):
                for name in dirs[:] + names:
                    path = Path(directory) / name
                    relative = path.relative_to(artifact).as_posix()
                    inspect_name(relative)
                    if linked(path):
                        errors.append(f"Delivery contains a link/reparse point: {relative}")
                        if name in dirs:
                            dirs.remove(name)
                    elif path.is_file():
                        files += 1
                    elif not path.is_dir():
                        errors.append(f"Unsupported delivery entry: {relative}")
        elif not artifact.is_file():
            return ["Delivery artifact must be a directory, ZIP or TAR file."]
        elif zipfile.is_zipfile(artifact):
            with zipfile.ZipFile(artifact) as archive:
                for member in archive.infolist():
                    inspect_name(member.filename)
                    kind = stat.S_IFMT(member.external_attr >> 16)
                    if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
                        errors.append(f"Unsupported delivery entry/link: {member.filename}")
                    elif not member.is_dir():
                        files += 1
        elif tarfile.is_tarfile(artifact):
            with tarfile.open(artifact, "r:*") as archive:
                for member in archive:
                    inspect_name(member.name)
                    if member.isfile():
                        files += 1
                    elif not member.isdir():
                        errors.append(f"Unsupported delivery entry/link: {member.name}")
        else:
            return ["Unsupported delivery artifact; provide a directory, ZIP or TAR file."]
    except (OSError, ValueError, EOFError, tarfile.TarError, zipfile.BadZipFile) as exc:
        errors.append(f"Could not inspect delivery artifact: {exc}")
    if not files:
        errors.append("Delivery artifact contains no regular files.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init_parser = commands.add_parser("init", help="Create new project records without overwriting.")
    init_parser.add_argument("--name", required=True)
    init_parser.add_argument("--mode", choices=("greenfield", "brownfield"), required=True)
    check_parser = commands.add_parser("check", help="Check structure and selected state rules.")
    check_parser.add_argument("--ready", action="store_true", help="Also flag unfinished task/handoff placeholders.")
    export_parser = commands.add_parser("export", help="Copy the framework without project records.")
    export_parser.add_argument("destination", type=Path)
    delivery_parser = commands.add_parser("check-delivery", help="Inspect a delivery directory or ZIP/TAR for .ai content.")
    delivery_parser.add_argument("artifact", type=Path)
    commands.add_parser("migrate-matrix", help="Losslessly split a legacy matrix into per-task files.")
    commands.add_parser("context", help="Show only active task record routes.")
    read_parser = commands.add_parser("read-record", help="Read a bounded byte page of a project record.")
    read_parser.add_argument("path")
    read_parser.add_argument("--offset", type=int, default=0)
    read_parser.add_argument("--limit", type=int, default=PAGE_BYTES)
    tasks_parser = commands.add_parser("tasks", help="List a bounded page of task IDs in lexical order.")
    tasks_parser.add_argument("--after", default="")
    tasks_parser.add_argument("--limit", type=int, default=20)
    commands.add_parser("memory-check", help="Check size limits for all working records.")
    args = parser.parse_args()
    ai_root = Path(__file__).resolve().parents[1]
    try:
        if args.command == "init":
            print(f"Initialized: {initialize(ai_root, args.name, args.mode)}")
            print("Draft records only. Continue with START_MANAGER.md.")
        elif args.command == "export":
            print(f"Clean framework exported: {export_clean(ai_root, args.destination)}")
        elif args.command == "migrate-matrix":
            print(migrate_matrix(ai_root / "project"))
        elif args.command == "context":
            print(json.dumps(context_routes(ai_root / "project"), indent=2))
        elif args.command == "read-record":
            page = read_record(ai_root / "project", args.path, args.offset, args.limit)
            content = page.pop("text")
            print(json.dumps(page))
            print(content)
        elif args.command == "tasks":
            print(json.dumps(task_page(ai_root / "project", args.after, args.limit)))
        else:
            if args.command == "check-delivery":
                errors = check_delivery(args.artifact)
            elif args.command == "memory-check":
                if not (ai_root / "project").is_dir():
                    raise ValueError("Initialize project records first.")
                errors = memory_issues(ai_root / "project")
            else:
                errors = check(ai_root, args.ready)
            if errors:
                for error in errors[:30]:
                    print(f"ERROR: {error[:400]}", file=sys.stderr)
                if len(errors) > 30:
                    print(f"{len(errors) - 30} further errors omitted; fix these and rerun.", file=sys.stderr)
                return 1
            if args.command == "check-delivery":
                print("Delivery name/type checks passed: no .ai entries. Nested archives, content and application completeness are not validated.")
            elif args.command == "memory-check":
                print("Working records are within size limits. Cold history/evidence must be read in pages.")
            else:
                print("Structural checks passed. Content, code correctness, and acceptance are not validated.")
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
