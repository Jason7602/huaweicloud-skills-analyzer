from src.llm.llm_factory import LlmFactory
from src.llm.openai_provider import OpenAIProvider
from src.llm.pangu_provider import PanguProvider
from src.models.llm_config import LlmConfig, LlmProvider


def test_create_openai_provider():
    config = LlmConfig(
        provider=LlmProvider.OPENAI,
        model_name="gpt-4o",
        api_key="sk-test",
    )
    factory = LlmFactory()
    provider = factory.create_provider(config)
    assert isinstance(provider, OpenAIProvider)


def test_create_pangu_provider():
    config = LlmConfig(
        provider=LlmProvider.PANGU,
        model_name="pangu-v2",
        api_key="test-key",
    )
    factory = LlmFactory()
    provider = factory.create_provider(config)
    assert isinstance(provider, PanguProvider)


def test_unknown_provider():
    config = LlmConfig(provider=LlmProvider.CUSTOM, api_key="test")
    factory = LlmFactory()
    try:
        factory.create_provider(config)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown LLM provider" in str(e)


def test_register_custom_provider():
    from src.llm.base_provider import BaseLlmProvider

    class MockProvider(BaseLlmProvider):
        def __init__(self, model_name="", api_key="", base_url="", temperature=0.1, max_tokens=4096, **kwargs):
            pass
        def invoke(self, prompt, **kwargs):
            return "mock"
        def invoke_with_structured_output(self, prompt, schema, **kwargs):
            return {}
        def is_available(self):
            return True
        def get_model_info(self):
            return {"provider": "mock"}

    LlmFactory.register_provider("custom", MockProvider)
    factory = LlmFactory()
    config = LlmConfig(provider=LlmProvider.CUSTOM, api_key="test")

    provider = factory.create_provider(config)
    assert isinstance(provider, MockProvider)