import tempfile
from pathlib import Path

from config import ConfigManager, load_yaml_config, find_default_config


def _write_config(tmp_dir: str, content: str, filename: str = "config.yaml") -> str:
    path = Path(tmp_dir) / filename
    path.write_text(content, encoding="utf-8")
    return str(path)


def test_load_yaml_config():
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, """
skills_repo: "/path/to/skills"
skill_names:
  - skill-a
  - skill-b
output_dir: "./custom-reports"
log_level: "DEBUG"
max_retries: 5
llm:
  provider: "pangu"
  model: "pangu-v2"
  api_key: "test-key"
  temperature: 0.5
""")
        data = load_yaml_config(path)
        assert data["skills_repo"] == "/path/to/skills"
        assert len(data["skill_names"]) == 2
        assert data["output_dir"] == "./custom-reports"
        assert data["llm"]["provider"] == "pangu"
        assert data["llm"]["api_key"] == "test-key"


def test_load_yaml_config_not_found():
    try:
        load_yaml_config("/nonexistent/config.yaml")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass


def test_config_from_file():
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, """
skills_repo: "/path/to/skills"
skill_names:
  - skill-a
output_dir: "./custom-reports"
log_level: "DEBUG"
max_retries: 5
llm:
  provider: "pangu"
  model: "pangu-v2"
  api_key: "test-pangu-key"
  temperature: 0.5
""")
        mgr = ConfigManager()
        config, llm_config = mgr.parse_args(["--config", path])

        assert config.skills_repo_path == "/path/to/skills"
        assert config.skill_names == ["skill-a"]
        assert config.output_dir == "./custom-reports"
        assert config.log_level == "DEBUG"
        assert config.max_retries == 5
        assert llm_config.provider.value == "pangu"
        assert llm_config.model_name == "pangu-v2"
        assert llm_config.api_key == "test-pangu-key"
        assert llm_config.temperature == 0.5


def test_cli_overrides_file():
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, """
skills_repo: "/file/path"
output_dir: "./file-reports"
log_level: "INFO"
llm:
  provider: "openai"
  model: "gpt-4o"
  api_key: "file-key"
""")
        mgr = ConfigManager()
        config, llm_config = mgr.parse_args([
            "--config", path,
            "--output-dir", "./cli-reports",
            "--log-level", "DEBUG",
            "--llm-api-key", "cli-key",
        ])

        assert config.skills_repo_path == "/file/path"
        assert config.output_dir == "./cli-reports"
        assert config.log_level == "DEBUG"
        assert llm_config.api_key == "cli-key"


def test_config_file_with_llm_disabled():
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, """
skills_repo: "/path/to/skills"
llm:
  disabled: true
""")
        mgr = ConfigManager()
        config, llm_config = mgr.parse_args(["--config", path])
        assert not llm_config.is_enabled


def test_config_file_defaults():
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, """
skills_repo: "/path/to/skills"
""")
        mgr = ConfigManager()
        config, llm_config = mgr.parse_args(["--config", path])

        assert config.sdk_cache_dir == "./cache/sdk-source"
        assert config.log_level == "INFO"
        assert config.max_retries == 3
        assert llm_config.provider.value == "openai"
        assert llm_config.model_name == "gpt-4o"


def test_no_llm_flag_overrides_file():
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, """
skills_repo: "/path/to/skills"
llm:
  provider: "openai"
  api_key: "file-key"
""")
        mgr = ConfigManager()
        config, llm_config = mgr.parse_args(["--config", path, "--no-llm"])
        assert not llm_config.is_enabled


def test_skills_repo_required():
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_config(tmp, """
output_dir: "./reports"
""")
        mgr = ConfigManager()
        try:
            mgr.parse_args(["--config", path])
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "skills_repo" in str(e)