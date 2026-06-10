from unittest.mock import MagicMock, patch

from src.llm.llm_client import LlmClient
from src.models.llm_config import LlmConfig, LlmProvider


def test_llm_client_not_available_without_key():
    config = LlmConfig(api_key="")
    client = LlmClient(config)
    assert not client.is_available


def test_llm_client_analyze_returns_none_when_unavailable():
    config = LlmConfig(api_key="")
    client = LlmClient(config)
    result = client.analyze("test prompt", "test_type")
    assert result is None


def test_llm_client_analyze_with_mock_provider():
    config = LlmConfig(provider=LlmProvider.OPENAI, api_key="sk-test", model_name="gpt-4o")
    client = LlmClient(config)

    mock_provider = MagicMock()
    mock_provider.is_available.return_value = True
    mock_provider.invoke.return_value = "LLM analysis result"
    mock_provider.get_model_info.return_value = {"model": "gpt-4o", "provider": "openai"}

    client._provider = mock_provider

    result = client.analyze("Analyze this skill", "business_logic")
    assert result is not None
    assert result.response == "LLM analysis result"
    assert result.analysis_type == "business_logic"
    assert result.model_used == "gpt-4o"


def test_llm_client_retry_on_failure():
    config = LlmConfig(provider=LlmProvider.OPENAI, api_key="sk-test", model_name="gpt-4o")
    client = LlmClient(config, max_retries=2)

    mock_provider = MagicMock()
    mock_provider.is_available.return_value = True
    mock_provider.invoke.side_effect = [Exception("API error"), "success response"]
    mock_provider.get_model_info.return_value = {"model": "gpt-4o", "provider": "openai"}

    client._provider = mock_provider

    result = client.analyze("test prompt", "test_type")
    assert result is not None
    assert result.response == "success response"
    assert mock_provider.invoke.call_count == 2


def test_llm_client_all_retries_fail():
    config = LlmConfig(provider=LlmProvider.OPENAI, api_key="sk-test", model_name="gpt-4o")
    client = LlmClient(config, max_retries=2)

    mock_provider = MagicMock()
    mock_provider.is_available.return_value = True
    mock_provider.invoke.side_effect = Exception("API error")

    client._provider = mock_provider

    result = client.analyze("test prompt", "test_type")
    assert result is None