from dataclasses import asdict

from src.models.llm_config import LlmAnalysisResult, LlmConfig, LlmProvider


def test_llm_provider_enum():
    assert LlmProvider.OPENAI.value == "openai"
    assert LlmProvider.PANGU.value == "pangu"
    assert LlmProvider.CUSTOM.value == "custom"


def test_llm_config_defaults():
    config = LlmConfig()
    assert config.provider == LlmProvider.OPENAI
    assert config.model_name == "gpt-4o"
    assert config.temperature == 0.1
    assert config.max_tokens == 4096
    assert not config.is_enabled


def test_llm_config_enabled():
    config = LlmConfig(api_key="sk-test-key")
    assert config.is_enabled


def test_llm_config_pangu():
    config = LlmConfig(provider=LlmProvider.PANGU, model_name="pangu-v2", api_key="test-key")
    assert config.provider == LlmProvider.PANGU
    assert config.model_name == "pangu-v2"
    assert config.is_enabled


def test_llm_config_serialization():
    config = LlmConfig(provider=LlmProvider.OPENAI, api_key="sk-test", model_name="gpt-4o")
    d = asdict(config)
    assert d["provider"] == "openai"
    assert d["api_key"] == "sk-test"


def test_llm_analysis_result():
    result = LlmAnalysisResult(
        analysis_type="business_logic",
        prompt="test prompt",
        response="test response",
        model_used="gpt-4o",
        token_usage={"input": 100, "output": 50},
        timestamp="2024-01-01T00:00:00Z",
    )
    d = asdict(result)
    assert d["analysis_type"] == "business_logic"
    assert d["token_usage"]["input"] == 100