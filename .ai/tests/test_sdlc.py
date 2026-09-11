"""Regression tests use disposable projects and never initialize the distribution."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest


SOURCE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sdlc", SOURCE / "tools" / "sdlc.py")
sdlc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sdlc)


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = sdlc.staging_directory(SOURCE.parent, ".sdlc-test-")
        self.root = self.temporary.__enter__()
        self.addCleanup(self.temporary.__exit__, None, None, None)
        self.ai = self.root / "first" / ".ai"
        sdlc.export_clean(SOURCE, self.ai)

    def init(self, mode="greenfield"):
        return sdlc.initialize(self.ai, "Example project", mode)

    def state(self, **updates):
        path = self.ai / "project" / "state.json"
        state = sdlc.read_json(path)
        state.update(updates)
        sdlc.write_json(path, state)

    def handoff(self, actor, task="TASK-001", number=1):
        (self.ai / "project" / "handoffs" / "current.md").write_text(
            f"ID: HANDOFF-{number:03d}\nTo: {actor}\nTask: {task}\nContract: {'none' if task == 'none' else 1}\n\n"
            "Read the active task and entry point; perform the next action.\n",
            encoding="utf-8",
        )

    def task(self, status):
        (self.ai / "project" / "tasks" / "TASK-001.md").write_text(
            f"ID: TASK-001\nStatus: {status}\nContract: 1\n\n"
            "Implement the specified calculator and verify its acceptance criteria.\n",
            encoding="utf-8",
        )
        path = self.ai / "project" / "task-matrix.json"
        matrix = sdlc.read_json(path)
        if not matrix["tasks"]:
            matrix["tasks"].append({
                "id": "TASK-001", "feature": "FEATURE-001", "revision": 1,
                "depends_on": [], "scope_review": "READY",
                "inventory_note": "Inspected the fixture calculator entry point and its boundary cases.",
                "reviewed_code_identity": "",
                "touchpoints": [{"id": "TP-001", "path": "calculator.py", "surface": "Public calculation entry point", "action": "CHANGE", "reason": "Implement required calculation behavior."}],
                "checks": [{"id": "CHK-001", "criterion": "AC-001", "scenario": "Calculate the boundary input through the public entry point.", "touchpoints": ["TP-001"], "mode": "AUTOMATED", "method": "Run the specified boundary-case test.", "expected": "Returns exactly the specified boundary value.", "result": {"status": "NOT_RUN", "contract_revision": 1, "code_identity": "", "reason": "Not executed yet.", "evidence": []}, "review": "PENDING"}],
            })
            sdlc.write_json(path, matrix)

    def matrix(self):
        return sdlc.read_json(self.ai / "project" / "task-matrix.json")

    def save_matrix(self, matrix):
        sdlc.write_json(self.ai / "project" / "task-matrix.json", matrix)

    def ready_worker(self):
        self.init()
        self.task("READY")
        self.state(active_role="worker", active_task="TASK-001", task_status="READY")
        self.handoff("worker")

    def pass_check(self):
        evidence = self.ai / "project" / "evidence" / "result.txt"
        evidence.write_text("Fixture execution record: CHK-001 passed in this structural simulation.", encoding="utf-8")
        matrix = self.matrix()
        task = matrix["tasks"][0]
        task["reviewed_code_identity"] = "fixture-snapshot-1"
        task["checks"][0]["result"] = {"status": "PASS", "contract_revision": 1, "code_identity": "fixture-snapshot-1", "reason": "", "evidence": [{"path": "evidence/result.txt", "locator": "CHK-001 execution record"}]}
        task["checks"][0]["review"] = "ACCEPTED"
        self.save_matrix(matrix)

    def test_greenfield_initialization_is_valid_and_draft(self):
        project = self.init()
        self.assertEqual([], sdlc.check(self.ai, ready=True))
        self.assertIn("DRAFT", (project / "brief.md").read_text())
        self.assertEqual("NOT_RUN", (project / "testing" / "uat.md").read_text().split("Overall status: ")[1].splitlines()[0])

    def test_brownfield_preserves_application(self):
        existing = self.ai.parent / "application.txt"
        existing.write_text("existing user work", encoding="utf-8")
        self.init("brownfield")
        self.assertEqual("existing user work", existing.read_text())
        self.assertEqual("brownfield", sdlc.read_json(self.ai / "project" / "config.json")["mode"])

    def test_reinitialization_refuses_to_overwrite(self):
        project = self.init()
        original = (project / "config.json").read_bytes()
        with self.assertRaises(ValueError):
            self.init("brownfield")
        self.assertEqual(original, (project / "config.json").read_bytes())

    def test_failed_initialization_leaves_no_partial_project(self):
        (self.ai / "framework" / "templates" / "brief.md").unlink()
        with self.assertRaises(OSError):
            self.init()
        self.assertFalse((self.ai / "project").exists())
        self.assertFalse(list(self.ai.glob(".init-*")))

    def test_uninitialized_check_reports_missing_project(self):
        self.assertIn("Initialize", sdlc.check(self.ai)[0])

    def test_clean_export_excludes_project_history(self):
        project = self.init()
        (project / "reports" / "private.md").write_text("project-only", encoding="utf-8")
        target = self.root / "second" / ".ai"
        sdlc.export_clean(self.ai, target)
        self.assertFalse((target / "project").exists())
        self.assertTrue((target / "START_MANAGER.md").is_file())
        sdlc.initialize(target, "Second", "brownfield")
        self.assertEqual([], sdlc.check(target))
        self.assertNotEqual(sdlc.read_json(project / "config.json")["project_id"], sdlc.read_json(target / "project" / "config.json")["project_id"])

    def test_export_refuses_existing_or_nested_destination(self):
        with self.assertRaises(ValueError):
            sdlc.export_clean(self.ai, self.ai)
        with self.assertRaises(ValueError):
            sdlc.export_clean(self.ai, self.ai / "nested" / ".ai")
        with self.assertRaises(ValueError):
            sdlc.export_clean(self.ai, self.root / "wrong-name")

    def test_copying_initialized_records_detects_wrong_project(self):
        self.init()
        target = self.root / "second" / ".ai"
        shutil.copytree(self.ai, target)
        self.assertTrue(any("root mismatch" in item for item in sdlc.check(target)))

    def test_full_manual_handoff_cycle(self):
        project = self.init()
        self.task("READY")
        self.state(active_role="worker", active_task="TASK-001", task_status="READY", stage="implementation")
        self.handoff("worker")
        self.assertEqual([], sdlc.check(self.ai, ready=True))
        self.task("IN_PROGRESS")
        self.state(task_status="IN_PROGRESS")
        self.assertEqual([], sdlc.check(self.ai, ready=True))
        self.task("SUBMITTED")
        self.state(active_role="manager", task_status="SUBMITTED", stage="verification")
        self.handoff("manager", number=2)
        self.assertTrue(any("worker report" in item for item in sdlc.check(self.ai)))
        (project / "reports" / "TASK-001-attempt-01.md").write_text("Example evidence for structural test only.")
        self.assertEqual([], sdlc.check(self.ai, ready=True))
        self.task("CHANGES_REQUESTED")
        self.state(active_role="worker", task_status="CHANGES_REQUESTED")
        self.handoff("worker", number=3)
        self.assertTrue(any("manager review" in item for item in sdlc.check(self.ai)))
        (project / "reviews" / "TASK-001-attempt-01.md").write_text("Correct the boundary case.")
        self.assertEqual([], sdlc.check(self.ai, ready=True))
        self.task("IN_PROGRESS")
        self.state(task_status="IN_PROGRESS")
        self.assertEqual([], sdlc.check(self.ai, ready=True))
        self.task("SUBMITTED")
        self.state(active_role="manager", task_status="SUBMITTED")
        self.handoff("manager", number=4)
        (project / "reports" / "TASK-001-attempt-02.md").write_text("Corrected boundary case; simulated evidence only.")
        self.assertEqual([], sdlc.check(self.ai, ready=True))
        self.task("ACCEPTED")
        self.state(active_role="manager", task_status="ACCEPTED")
        (project / "reviews" / "TASK-001-attempt-02.md").write_text("Accepted in structural simulation only.")
        self.pass_check()
        self.handoff("manager", number=5)
        self.assertEqual([], sdlc.check(self.ai, ready=True))

    def test_inconsistent_handoff_and_task_are_detected(self):
        self.init()
        self.task("READY")
        self.state(active_role="worker", active_task="TASK-001", task_status="IN_PROGRESS")
        errors = sdlc.check(self.ai)
        self.assertTrue(any("metadata disagrees" in error for error in errors))
        self.assertTrue(any("recipient disagrees" in error for error in errors))
        self.assertTrue(any("handoff task disagrees" in error for error in errors))

    def test_human_decision_before_task_is_valid(self):
        self.init()
        self.state(active_role="human")
        self.handoff("human", task="none")
        self.assertEqual([], sdlc.check(self.ai, ready=True))

    def test_placeholders_block_worker_dispatch(self):
        self.init()
        self.task("READY")
        self.state(active_role="worker", active_task="TASK-001", task_status="READY")
        self.handoff("worker")
        with (self.ai / "project" / "tasks" / "TASK-001.md").open("a") as handle:
            handle.write("TODO acceptance criteria")
        self.assertEqual([], sdlc.check(self.ai))
        self.assertTrue(any("placeholders" in error for error in sdlc.check(self.ai, ready=True)))

    def test_invalid_task_path_is_not_followed(self):
        self.init()
        self.state(active_task="../../outside", task_status="READY")
        self.assertTrue(any("Invalid active_task" in error for error in sdlc.check(self.ai)))

    def test_malformed_json_is_reported(self):
        project = self.init()
        (project / "state.json").write_text("{ broken", encoding="utf-8")
        self.assertTrue(sdlc.check(self.ai))

    def test_model_labels_are_replaceable(self):
        project = self.init()
        config = sdlc.read_json(project / "config.json")
        config["roles"]["manager"]["model"] = "Future manager"
        config["roles"]["worker"]["model"] = "Future worker"
        sdlc.write_json(project / "config.json", config)
        self.assertEqual([], sdlc.check(self.ai))

    def test_schema_and_timestamp_are_checked(self):
        self.init()
        self.state(schema_version=2, updated_at="yesterday")
        errors = sdlc.check(self.ai)
        self.assertTrue(any("schema_version" in error for error in errors))
        self.assertTrue(any("UTC timestamp" in error for error in errors))

    def test_cli_works_from_another_directory(self):
        command = [sys.executable, str(self.ai / "tools" / "sdlc.py")]
        initialized = subprocess.run(command + ["init", "--name", "CLI project", "--mode", "brownfield"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(0, initialized.returncode, initialized.stderr)
        checked = subprocess.run(command + ["check", "--ready"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(0, checked.returncode, checked.stderr)
        self.assertIn("not validated", checked.stdout)

    def test_manager_readiness_required_before_worker_execution(self):
        self.ready_worker()
        matrix = self.matrix()
        matrix["tasks"][0]["scope_review"] = "DRAFT"
        self.save_matrix(matrix)
        self.assertTrue(any("scope review" in error for error in sdlc.check(self.ai, ready=True)))

    def test_uncovered_touchpoint_blocks_handoff(self):
        self.ready_worker()
        matrix = self.matrix()
        matrix["tasks"][0]["touchpoints"].append({"id": "TP-UPGRADE", "path": "migrations.py", "surface": "Upgrade existing data", "action": "CHANGE", "reason": "Existing installations must remain compatible."})
        self.save_matrix(matrix)
        self.assertTrue(any("uncovered touchpoint" in error for error in sdlc.check(self.ai, ready=True)))

    def test_contract_revision_disagreement_is_rejected(self):
        self.ready_worker()
        matrix = self.matrix()
        matrix["tasks"][0]["revision"] = 2
        self.save_matrix(matrix)
        errors = sdlc.check(self.ai, ready=True)
        self.assertTrue(any("task Contract" in error for error in errors))
        self.assertTrue(any("handoff Contract" in error for error in errors))

    def test_changed_contract_rejects_stale_passing_result(self):
        self.ready_worker()
        self.pass_check()
        matrix = self.matrix()
        matrix["tasks"][0]["revision"] = 2
        self.save_matrix(matrix)
        self.assertTrue(any("result contract revision" in error for error in sdlc.check(self.ai)))

    def test_missing_matrix_task_is_rejected(self):
        self.ready_worker()
        self.save_matrix({"schema_version": 1, "tasks": []})
        self.assertTrue(any("missing from matrix" in error for error in sdlc.check(self.ai)))

    def test_dependency_cycle_and_unaccepted_dependency_are_rejected(self):
        self.ready_worker()
        matrix = self.matrix()
        first = matrix["tasks"][0]
        second = json.loads(json.dumps(first))
        second["id"] = "TASK-002"
        second["depends_on"] = ["TASK-001"]
        first["depends_on"] = ["TASK-002"]
        matrix["tasks"].append(second)
        (self.ai / "project" / "tasks" / "TASK-002.md").write_text("ID: TASK-002\nStatus: READY\nContract: 1\n\nSecond task.\n")
        self.save_matrix(matrix)
        errors = sdlc.check(self.ai, ready=True)
        self.assertTrue(any("Dependency cycle" in error for error in errors))
        self.assertTrue(any("not ACCEPTED" in error for error in errors))

    def test_unknown_dependency_is_rejected(self):
        self.ready_worker()
        matrix = self.matrix()
        matrix["tasks"][0]["depends_on"] = ["TASK-099"]
        self.save_matrix(matrix)
        self.assertTrue(any("unknown dependency" in error for error in sdlc.check(self.ai)))

    def test_empty_evidence_cannot_support_pass(self):
        self.ready_worker()
        self.pass_check()
        (self.ai / "project" / "evidence" / "result.txt").write_text("")
        self.assertTrue(any("empty evidence" in error for error in sdlc.check(self.ai)))

    def test_outside_evidence_path_is_rejected(self):
        self.ready_worker()
        self.pass_check()
        matrix = self.matrix()
        matrix["tasks"][0]["checks"][0]["result"]["evidence"][0]["path"] = "../../outside.txt"
        self.save_matrix(matrix)
        self.assertTrue(any("inside project records" in error for error in sdlc.check(self.ai)))

    def test_acceptance_requires_every_check_to_be_reviewed(self):
        self.ready_worker()
        project = self.ai / "project"
        self.task("ACCEPTED")
        self.state(active_role="manager", task_status="ACCEPTED")
        self.handoff("manager")
        (project / "reports" / "TASK-001-attempt-01.md").write_text("Worker claims completion.")
        (project / "reviews" / "TASK-001-attempt-01.md").write_text("Review artifact exists.")
        errors = sdlc.check(self.ai)
        self.assertTrue(any("task acceptance requires" in error for error in errors))
        self.pass_check()
        self.assertEqual([], sdlc.check(self.ai))
        matrix = self.matrix()
        matrix["tasks"][0]["checks"][0]["review"] = "PENDING"
        self.save_matrix(matrix)
        self.assertTrue(any("task acceptance requires" in error for error in sdlc.check(self.ai)))

    def test_acceptance_rejects_wrong_code_identity(self):
        self.ready_worker()
        self.task("ACCEPTED")
        self.state(active_role="manager", task_status="ACCEPTED")
        self.handoff("manager")
        self.pass_check()
        matrix = self.matrix()
        matrix["tasks"][0]["reviewed_code_identity"] = "different-snapshot"
        self.save_matrix(matrix)
        self.assertTrue(any("differs from manager-reviewed" in error for error in sdlc.check(self.ai)))

    def test_duplicate_check_id_is_rejected(self):
        self.ready_worker()
        matrix = self.matrix()
        matrix["tasks"][0]["checks"].append(matrix["tasks"][0]["checks"][0].copy())
        self.save_matrix(matrix)
        self.assertTrue(any("duplicate check ID" in error for error in sdlc.check(self.ai)))


if __name__ == "__main__":
    unittest.main()
