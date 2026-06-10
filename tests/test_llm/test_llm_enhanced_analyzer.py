from unittest.mock import MagicMock

from src.analyzers.llm_enhanced_analyzer import LlmEnhancedAnalyzer
from src.llm.llm_client import LlmClient
from src.models.api_interface import ApiInterface
from src.models.cli_command import CliCommand
from src.models.cli_gap import AlternativeScheme, CliGap
from src.models.enums import HttpMethod, ImpactLevel, IsMandatory, AlternativeFeasibility
from src.models.llm_config import LlmAnalysisResult, LlmConfig
from src.models.report import SkillAnalysisResult
from src.models.skill import SkillImplResult
from src.models.enums import ImplType


def _make_llm_client_with_mock(response_text="AI analysis result"):
    config = LlmConfig(api_key="sk-test")
    client = LlmClient(config)

    mock_provider = MagicMock()
    mock_provider.is_available.return_value = True
    mock_provider.invoke.return_value = response_text
    mock_provider.get_model_info.return_value = {"model": "gpt-4o", "provider": "openai"}

    client._provider = mock_provider
    return client


def test_analyze_business_logic():
    client = _make_llm_client_with_mock()
    analyzer = LlmEnhancedAnalyzer(client)

    skill_info = SkillImplResult(
        skill_name="test-skill",
        implementation_type=ImplType.SDK,
        source_path="/path",
        business_goal="Test goal",
    )
    api_interfaces = [ApiInterface(
        service_name="ECS", api_name="CreateInstance",
        api_path="/v1/cloudservers", http_method=HttpMethod.POST,
    )]

    result = analyzer.analyze_business_logic(skill_info, api_interfaces)
    assert result is not None
    assert result.analysis_type == "business_logic"
    assert "AI analysis result" in result.response


def test_evaluate_alternative_feasibility():
    client = _make_llm_client_with_mock("部分可行")
    analyzer = LlmEnhancedAnalyzer(client)

    gap = CliGap(
        unsupported_api="ListByTags",
        service_name="ECS",
        business_role="Query by tags",
        impact_level=ImpactLevel.IMPORTANT,
        is_mandatory=IsMandatory.MANDATORY,
    )
    alt = AlternativeScheme(
        unsupported_api="ListByTags",
        alternative_cli="hcloud ecs ListServers",
        feasibility=AlternativeFeasibility.PARTIAL,
    )

    result = analyzer.evaluate_alternative_feasibility(gap, alt)
    assert result is not None
    assert result.analysis_type == "alternative_feasibility"


def test_suggest_alternatives():
    client = _make_llm_client_with_mock("建议使用 hcloud ecs ListServers")
    analyzer = LlmEnhancedAnalyzer(client)

    gap = CliGap(
        unsupported_api="ListByTags",
        service_name="ECS",
        business_role="Query by tags",
        impact_level=ImpactLevel.IMPORTANT,
        is_mandatory=IsMandatory.MANDATORY,
    )
    cmds = [CliCommand(
        cli_command="hcloud ecs ListServers",
        corresponding_api="ListServers",
        cli_service="ecs",
    )]

    result = analyzer.suggest_alternatives(gap, cmds)
    assert result is not None
    assert result.analysis_type == "suggest_alternatives"


def test_summarize_analysis():
    client = _make_llm_client_with_mock("总体评估：该Skill CLI兼容性一般")
    analyzer = LlmEnhancedAnalyzer(client)

    skill_result = SkillAnalysisResult(
        skill_info=SkillImplResult(
            skill_name="test-skill",
            implementation_type=ImplType.SDK,
            source_path="/path",
        ),
    )

    result = analyzer.summarize_analysis(skill_result)
    assert result is not None
    assert result.analysis_type == "analysis_summary"


def test_degrade_when_llm_unavailable():
    config = LlmConfig(api_key="")
    client = LlmClient(config)
    analyzer = LlmEnhancedAnalyzer(client)

    skill_info = SkillImplResult(
        skill_name="test", implementation_type=ImplType.SDK, source_path="/path"
    )
    result = analyzer.analyze_business_logic(skill_info, [])
    assert result is None