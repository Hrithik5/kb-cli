from pathlib import Path

from kb.database import Database
from kb.models.knowledge import KnowledgeItem
from kb.repositories.knowledge_repository import KnowledgeRepository


def create_test_repo():
    db = Database(Path(":memory:"))
    db.init_schema()
    return KnowledgeRepository(db)


def test_add_and_get_by_id(repo=None):
    if repo is None:
        repo = create_test_repo()
    item = KnowledgeItem(category="git", title="Delete branch", content="git branch -D feature", tags=["git", "branch"])
    saved = repo.add(item)
    assert saved.id is not None
    assert saved.id > 0

    fetched = repo.get_by_id(saved.id)
    assert fetched is not None
    assert fetched.category == "git"
    assert fetched.title == "Delete branch"
    assert fetched.content == "git branch -D feature"
    assert fetched.tags == ["git", "branch"]


def test_fts5_search(repo=None):
    if repo is None:
        repo = create_test_repo()
    repo.add(KnowledgeItem(category="git", title="Delete local branch", content="git branch -D feature", tags=["git"]))
    repo.add(KnowledgeItem(category="docker", title="Start compose", content="docker compose up -d", tags=["docker"]))

    results = repo.find("compose")
    assert len(results) == 1
    assert results[0].category == "docker"
    assert "compose" in results[0].content

    results_git = repo.find("branch")
    assert len(results_git) == 1
    assert results_git[0].category == "git"


def test_update_and_delete(repo=None):
    if repo is None:
        repo = create_test_repo()
    item = repo.add(KnowledgeItem(category="python", title="List comp", content="[x for x in range(10)]"))
    item.title = "List comprehension"
    repo.update(item)

    updated = repo.get_by_id(item.id)
    assert updated.title == "List comprehension"

    deleted = repo.delete(item.id)
    assert deleted is True
    assert repo.get_by_id(item.id) is None


def test_toggle_favorite_and_stats(repo=None):
    if repo is None:
        repo = create_test_repo()
    item = repo.add(KnowledgeItem(category="git", title="Rebase", content="git rebase -i HEAD~5"))
    fav_status = repo.toggle_favorite(item.id)
    assert fav_status is True

    favs = repo.get_favorites()
    assert len(favs) == 1
    assert favs[0].id == item.id

    stats = repo.get_stats()
    assert stats["total_items"] == 1
    assert stats["favorite_items"] == 1
    assert "git" in stats["categories"]
