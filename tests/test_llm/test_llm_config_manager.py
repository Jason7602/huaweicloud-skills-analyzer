import os
from unittest.mock import patch

from src.llm.llm_config_manager import LlmConfigManager
from src.models.llm_config import LlmProvider


def test_default_config():
    mgr = LlmConfigManager()
    config = mgr.get_config()
    assert config.provider == LlmProvider.OPENAI
    assert not config.is_enabled


def test_no_llm_flag():
    mgr = LlmConfigManager()
    config = mgr.get_config(no_llm=True)
    assert not config.is_enabled
    assert config.api_key == ""


def test_cli_args_override():
    mgr = LlmConfigManager()
    config = mgr.get_config(
        provider="openai",
        model_name="gpt-4o-mini",
        api_key="sk-test-key",
    )
    assert config.provider == LlmProvider.OPENAI
    assert config.model_name == "gpt-4o-mini"
    assert config.is_enabled


def test_pangu_provider_config():
    mgr = LlmConfigManager()
    config = mgr.get_config(provider="pangu", api_key="pangu-key")
    assert config.provider == LlmProvider.PANGU
    assert config.is_enabled


def test_env_vars():
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "openai",
        "LLM_MODEL": "gpt-4o-mini",
        "LLM_API_KEY": "sk-env-key",
    }):
        mgr = LlmConfigManager()
        config = mgr.get_config()
        assert config.model_name == "gpt-4o-mini"
        assert config.api_key == "sk-env-key"
        assert config.is_enabled


def test_cli_overrides_env():
    with patch.dict(os.environ, {"LLM_API_KEY": "sk-env-key"}):
        mgr = LlmConfigManager()
        config = mgr.get_config(api_key="sk-cli-key")
        assert config.api_key == "sk-cli-key"


def test_is_llm_enabled():
    mgr = LlmConfigManager()
    config_enabled = mgr.get_config(api_key="sk-test")
    config_disabled = mgr.get_config()
    assert mgr.is_llm_enabled(config_enabled)
    assert not mgr.is_llm_enabled(config_disabled)