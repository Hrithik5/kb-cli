import json

from kb.database import Database
from kb.repositories.knowledge_repository import KnowledgeRepository
from kb.services.import_export_service import ImportExportService
from kb.services.knowledge_service import KnowledgeService


def create_test_import_export(tmp_path):
    db_path = tmp_path / "test.db"
    db = Database(db_path)
    db.init_schema()
    repo = KnowledgeRepository(db)
    service = KnowledgeService(repo)
    return ImportExportService(service), service, db_path, tmp_path


def test_markdown_import_export(tmp_path):
    service_ie, service, db_path, tmp_path = create_test_import_export(tmp_path)

    md_file = tmp_path / "sample.md"
    md_file.write_text("# Git Commands\n\n### Branch Delete\ngit branch -D feature\n\n# Docker Commands\n\ndocker compose up", encoding="utf-8")

    imported = service_ie.import_markdown_file(md_file)
    assert len(imported) >= 1

    export_md = tmp_path / "out.md"
    count = service_ie.export_markdown(export_md)
    assert count >= 1
    assert export_md.exists()
    assert "Knowledge Base Export" in export_md.read_text(encoding="utf-8")


def test_json_export(tmp_path):
    service_ie, service, db_path, tmp_path = create_test_import_export(tmp_path)
    service.add_item(category="k8s", content="kubectl get pods", title="Get Pods")

    json_file = tmp_path / "out.json"
    count = service_ie.export_json(json_file)
    assert count == 1
    assert json_file.exists()

    data = json.loads(json_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["category"] == "k8s"
    assert data[0]["content"] == "kubectl get pods"
