from pathlib import Path

from kb.database import Database
from kb.repositories.knowledge_repository import KnowledgeRepository
from kb.services.knowledge_service import KnowledgeService


def create_test_service():
    db = Database(Path(":memory:"))
    db.init_schema()
    repo = KnowledgeRepository(db)
    return KnowledgeService(repo)


def test_add_item_validation(service=None):
    if service is None:
        service = create_test_service()

    try:
        service.add_item(category="", content="test")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Category cannot be empty" in str(e)

    try:
        service.add_item(category="git", content="  ")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Content cannot be empty" in str(e)

    item = service.add_item(category="Git ", content="git checkout -b main", tags="git, checkout ")
    assert item.category == "git"
    assert item.tags == ["git", "checkout"]


def test_find_and_access_tracking(service=None):
    if service is None:
        service = create_test_service()

    item = service.add_item(category="docker", content="docker ps -a", title="List containers")
    assert item.access_count == 0

    results = service.find_items("containers", track_access=True)
    assert len(results) == 1
    assert results[0].id == item.id

    fetched = service.get_item(item.id)
    assert fetched.access_count == 1


def test_edit_service(service=None):
    if service is None:
        service = create_test_service()

    item = service.add_item(category="sh", content="echo hello", title="Echo")
    updated = service.edit_item(item.id, title="Echo hello world", tags=["bash", "sh"])
    assert updated.title == "Echo hello world"
    assert updated.tags == ["bash", "sh"]
