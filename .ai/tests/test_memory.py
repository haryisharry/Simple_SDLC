"""Scalability, bounded retrieval and lossless migration regressions."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

SOURCE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("memory_sdlc", SOURCE / "tools" / "sdlc.py")
sdlc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sdlc)


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = sdlc.staging_directory(SOURCE.parent, ".sdlc-test-")
        self.root = self.temporary.__enter__()
        self.addCleanup(self.temporary.__exit__, None, None, None)
        self.ai = self.root / "sample" / ".ai"
        sdlc.export_clean(SOURCE, self.ai)
        self.project = sdlc.initialize(self.ai, "Memory fixture", "brownfield")

    def task(self, number, depends=None):
        task_id = f"TASK-{number:04d}"
        (self.project / "tasks" / f"{task_id}.md").write_text(f"ID: {task_id}\nStatus: DRAFT\nContract: 1\n\nPlanned fixture.\n", encoding="utf-8")
        return {"id": task_id, "revision": 1, "depends_on": depends or [],
                "scope_review": "DRAFT", "touchpoints": [], "checks": []}

    def legacy(self, tasks):
        (self.project / "task-matrices").rmdir()
        value = {"schema_version": 1, "tasks": tasks}
        sdlc.write_json(self.project / "task-matrix.json", value)
        return value

    def test_large_migration_preserves_every_field_and_original_bytes(self):
        tasks = [self.task(i) for i in range(1500)]
        tasks[0]["custom_notes"] = {"evidence": ["preserve unknown nested fields"], "review": "historical"}
        original = self.legacy(tasks)
        before = (self.project / "task-matrix.json").read_bytes()
        self.assertGreater(len(before.splitlines()), 10000)
        records_before = {p.name: p.read_bytes() for p in (self.project / "tasks").glob("*.md")}
        self.assertTrue(any("Memory budget" in e for e in sdlc.check(self.ai)))
        sdlc.migrate_matrix(self.project)
        self.assertEqual(before, (self.project / "task-matrices" / "legacy-v1.json").read_bytes())
        self.assertEqual(original, sdlc.load_task_matrix(self.project))
        self.assertLess((self.project / "task-matrix.json").stat().st_size, 100)
        self.assertEqual(records_before, {p.name: p.read_bytes() for p in (self.project / "tasks").glob("*.md")})
        self.assertEqual([], sdlc.check(self.ai))
        self.assertIn("nothing changed", sdlc.migrate_matrix(self.project))

    def test_migration_resumes_after_descriptor_failure(self):
        original = self.legacy([self.task(1)])
        with mock.patch.object(sdlc.os, "replace", side_effect=OSError("interrupted commit")):
            with self.assertRaises(OSError):
                sdlc.migrate_matrix(self.project)
        self.assertEqual(original, sdlc.read_json(self.project / "task-matrix.json"))
        sdlc.migrate_matrix(self.project)
        self.assertEqual(original, sdlc.load_task_matrix(self.project))

    def test_migration_refuses_conflicts_and_unknown_top_level_fields(self):
        original = self.legacy([self.task(1)])
        original["unexpected"] = "must not be lost"
        sdlc.write_json(self.project / "task-matrix.json", original)
        with self.assertRaises(ValueError):
            sdlc.migrate_matrix(self.project)
        self.assertFalse((self.project / "task-matrices").exists())
        del original["unexpected"]
        sdlc.write_json(self.project / "task-matrix.json", original)
        target = self.project / "task-matrices"
        target.mkdir()
        (target / "unrelated.json").write_text("{}", encoding="utf-8")
        with self.assertRaises(ValueError):
            sdlc.migrate_matrix(self.project)
        self.assertEqual(original, sdlc.read_json(self.project / "task-matrix.json"))
        self.assertTrue((target / "unrelated.json").exists())

    def test_legacy_matrix_still_receives_structural_validation(self):
        self.legacy([self.task(1, ["TASK-9999"])])
        self.assertTrue(any("unknown dependency" in e for e in sdlc.check(self.ai)))

    def test_deep_dependency_chain_and_cycle_do_not_recurse(self):
        for i in range(1200):
            task = self.task(i, [f"TASK-{i+1:04d}"] if i < 1199 else [])
            sdlc.write_json(self.project / "task-matrices" / f"{task['id']}.json", task)
        self.assertEqual([], sdlc.check(self.ai))
        path = self.project / "task-matrices" / "TASK-1199.json"
        task = sdlc.read_json(path)
        task["depends_on"] = ["TASK-0000"]
        sdlc.write_json(path, task)
        self.assertTrue(any("Dependency cycle" in e for e in sdlc.check(self.ai)))

    def test_context_never_loads_unrelated_shards(self):
        state = sdlc.read_json(self.project / "state.json")
        state["active_task"] = "TASK-0001"
        sdlc.write_json(self.project / "state.json", state)
        (self.project / "task-matrices" / "TASK-9999.json").write_text("invalid unrelated content", encoding="utf-8")
        with mock.patch.object(sdlc, "load_task_matrix", side_effect=AssertionError("full matrix loaded")):
            routes = sdlc.context_routes(self.project)
        self.assertIn("task-matrices/TASK-0001.json", routes["read_next"])
        self.assertNotIn("TASK-9999", json.dumps(routes))
        self.assertLess(len(json.dumps(routes)), 1000)

    def test_all_working_file_types_are_bounded_and_history_is_paged(self):
        for relative, content in [("decisions.md", "x\n" * 121), ("custom.dat", b"x" * 8193),
                                  ("reports/large.md", "x\n" * 601), ("task-matrices/TASK-0001.json", " " * 49153)]:
            path = self.project / relative
            path.write_bytes(content.encode() if isinstance(content, str) else content)
        errors = sdlc.check(self.ai, ready=True)
        self.assertEqual(4, len(errors))
        self.assertTrue(all("Memory budget exceeded" in e for e in errors))
        raw = self.project / "evidence" / "long.log"
        raw.write_bytes(b"x" * 50000)
        first = sdlc.read_record(self.project, "evidence/long.log")
        second = sdlc.read_record(self.project, "evidence/long.log", first["next_offset"])
        self.assertEqual(12000, len(first["text"]))
        self.assertEqual(24000, second["next_offset"])
        self.assertTrue(second["more"])
        self.assertFalse(any("long.log" in e for e in sdlc.memory_issues(self.project)))

    def test_read_bounds_and_path_escape_are_rejected(self):
        for path, offset, limit in [("../outside", 0, 10), ("state.json", -1, 10), ("state.json", 0, 12001)]:
            with self.subTest(path=path, offset=offset, limit=limit), self.assertRaises(ValueError):
                sdlc.read_record(self.project, path, offset, limit)

    def test_shard_identity_and_missing_shard_are_detected(self):
        task = self.task(1)
        self.assertTrue(any("missing from matrix" in e for e in sdlc.check(self.ai)))
        sdlc.write_json(self.project / "task-matrices" / "TASK-0002.json", task)
        self.assertTrue(any("filename/ID mismatch" in e for e in sdlc.check(self.ai)))

    def test_task_listing_uses_nonoverlapping_bounded_pages(self):
        for i in range(75):
            self.task(i)
        collected, cursor = [], ""
        while True:
            page = sdlc.task_page(self.project, cursor, 20)
            self.assertLessEqual(len(page["tasks"]), 20)
            collected.extend(page["tasks"])
            if page["after"] is None:
                break
            cursor = page["after"]
        self.assertEqual(75, len(set(collected)))
        self.assertEqual(sorted(set(collected)), collected)

    def test_cli_caps_diagnostics_and_read_payload(self):
        for i in range(60):
            (self.project / f"long-{i}.md").write_bytes(b"x" * 9000)
        command = [sys.executable, str(self.ai / "tools" / "sdlc.py")]
        checked = subprocess.run(command + ["memory-check"], capture_output=True, text=True)
        self.assertEqual(1, checked.returncode)
        self.assertEqual(30, checked.stderr.count("ERROR:"))
        self.assertIn("further errors omitted", checked.stderr)
        (self.project / "evidence" / "large.log").write_bytes(b"x" * 100000)
        read = subprocess.run(command + ["read-record", "evidence/large.log"], capture_output=True, text=True)
        self.assertEqual(0, read.returncode, read.stderr)
        self.assertLess(len(read.stdout), 12500)


if __name__ == "__main__":
    unittest.main()
