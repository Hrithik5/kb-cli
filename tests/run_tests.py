#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.test_database import *
from tests.test_repository import *
from tests.test_service import *
from tests.test_cli import *
from tests.test_import_export import *


class TestRunner(unittest.TestCase):
    def test_database_flow(self):
        test_in_memory_database()
        test_schema_initialization()
        test_fts5_support()

    def test_repository_flow(self):
        db = Database(Path(":memory:"))
        db.init_schema()
        repo = KnowledgeRepository(db)
        test_add_and_get_by_id(repo)

        db2 = Database(Path(":memory:"))
        db2.init_schema()
        repo2 = KnowledgeRepository(db2)
        test_fts5_search(repo2)

        db3 = Database(Path(":memory:"))
        db3.init_schema()
        repo3 = KnowledgeRepository(db3)
        test_update_and_delete(repo3)

        db4 = Database(Path(":memory:"))
        db4.init_schema()
        repo4 = KnowledgeRepository(db4)
        test_toggle_favorite_and_stats(repo4)

    def test_service_flow(self):
        db = Database(Path(":memory:"))
        db.init_schema()
        repo = KnowledgeRepository(db)
        service = KnowledgeService(repo)

        test_add_item_validation(service)
        test_find_and_access_tracking(service)
        test_edit_service(service)

    def test_import_export_flow(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            db_path = tmp_path / "test.db"
            db = Database(db_path)
            db.init_schema()
            repo = KnowledgeRepository(db)
            service = KnowledgeService(repo)
            ie_tuple = (ImportExportService(service), service, db_path, tmp_path)

            test_markdown_import_export(ie_tuple)
            test_json_export(ie_tuple)

    def test_cli_flow(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            config_file = tmp_path / "config.toml"
            db_file = tmp_path / "kb_test.db"
            config_file.write_text(f'database = "{db_file}"\n', encoding="utf-8")

            assert run_cli(["--config-file", str(config_file), "init"]) == 0
            assert run_cli(["--config-file", str(config_file), "add", "git", "git status", "-t", "Status", "--tags", "git,status"]) == 0
            assert run_cli(["--config-file", str(config_file), "find", "status"]) == 0
            assert run_cli(["--config-file", str(config_file), "stats"]) == 0
            assert run_cli(["--config-file", str(config_file), "delete", "1"]) == 0


if __name__ == "__main__":
    unittest.main()
