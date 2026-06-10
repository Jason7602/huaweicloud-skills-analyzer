import tempfile
from pathlib import Path

from src.resources.skills_repo_manager import SkillsRepoManager


def test_list_skill_names():
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "skill-a").mkdir()
        (Path(tmp) / "skill-b").mkdir()
        mgr = SkillsRepoManager(tmp)
        names = mgr.list_skill_names()
        assert "skill-a" in names
        assert "skill-b" in names


def test_read_skill_files():
    with tempfile.TemporaryDirectory() as tmp:
        skill_dir = Path(tmp) / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "main.py").write_text("print('hello')", encoding="utf-8")
        mgr = SkillsRepoManager(tmp)
        files = mgr.read_skill_files("test-skill")
        assert any("main.py" in k for k in files)


def test_read_skill_config_from_readme():
    with tempfile.TemporaryDirectory() as tmp:
        skill_dir = Path(tmp) / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "README.md").write_text("# Test Skill\n\nThis is a test skill.\n", encoding="utf-8")
        mgr = SkillsRepoManager(tmp)
        config = mgr.read_skill_config("test-skill")
        assert "test" in config.get("description", "").lower()


def test_nonexistent_repo():
    mgr = SkillsRepoManager("/nonexistent/path")
    assert mgr.list_skill_names() == []