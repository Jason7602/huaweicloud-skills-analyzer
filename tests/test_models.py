from dataclasses import asdict

from src.models.enums import (
    AlternativeFeasibility,
    AnalysisStatus,
    CliCoveredStatus,
    HttpMethod,
    ImpactLevel,
    ImplType,
    IsMandatory,
    StepStatus,
)
from src.models.api_interface import ApiInterface, ApiParameter, SdkCallInfo
from src.models.cli_command import CliCommand, CliCoverageStatus
from src.models.cli_gap import AlternativeScheme, CliGap
from src.models.report import (
    AnalysisConfig,
    CliCoverageResult,
    ReportOutput,
    SdkAnalysisResult,
    SkillAnalysisResult,
)
from src.models.skill import SkillImplResult
from src.models.checkpoint import CheckpointInfo


def test_enums():
    assert ImplType.KOOCLI.value == "KooCLI"
    assert ImplType.SDK.value == "SDK"
    assert ImplType.HYBRID.value == "HYBRID"
    assert ImplType.UNKNOWN.value == "UNKNOWN"

    assert AnalysisStatus.COMPLETED.value == "completed"
    assert HttpMethod.POST.value == "POST"
    assert CliCoveredStatus.COVERED.value == "covered"
    assert ImpactLevel.CRITICAL.value == "critical"
    assert IsMandatory.MANDATORY.value == "mandatory"
    assert AlternativeFeasibility.FULL.value == "full"
    assert StepStatus.RUNNING.value == "running"


def test_skill_impl_result():
    result = SkillImplResult(
        skill_name="test-skill",
        implementation_type=ImplType.SDK,
        source_path="/path/to/skill",
        business_goal="Test goal",
        cli_evidence=["hcloud ecs list"],
        sdk_evidence=["from huaweicloudsdkecs"],
    )
    d = asdict(result)
    assert d["skill_name"] == "test-skill"
    assert d["implementation_type"] == "SDK"
    assert len(d["cli_evidence"]) == 1


def test_api_interface():
    api = ApiInterface(
        service_name="ECS",
        api_name="CreateInstance",
        api_path="/v1/{project_id}/cloudservers",
        http_method=HttpMethod.POST,
        required_params=[ApiParameter(name="name", param_type="str", is_required=True)],
        optional_params=[ApiParameter(name="adminPass", param_type="str", is_required=False)],
    )
    d = asdict(api)
    assert d["service_name"] == "ECS"
    assert len(d["required_params"]) == 1
    assert len(d["optional_params"]) == 1


def test_sdk_call_info():
    call = SdkCallInfo(
        service_name="ECS",
        client_class="EcsClient",
        method_name="create_instance",
        call_arguments={"name": "test"},
    )
    d = asdict(call)
    assert d["method_name"] == "create_instance"


def test_cli_command():
    cmd = CliCommand(
        cli_command="hcloud ecs CreateInstance",
        corresponding_api="CreateInstance",
        cli_service="ecs",
    )
    d = asdict(cmd)
    assert d["cli_service"] == "ecs"


def test_cli_coverage_status():
    status = CliCoverageStatus(
        api_name="CreateInstance",
        is_covered=CliCoveredStatus.COVERED,
    )
    assert status.is_covered == CliCoveredStatus.COVERED


def test_cli_gap():
    gap = CliGap(
        unsupported_api="ListResourcesByTags",
        service_name="ECS",
        business_role="Query resources by tags",
        impact_level=ImpactLevel.IMPORTANT,
        is_mandatory=IsMandatory.MANDATORY,
    )
    d = asdict(gap)
    assert d["unsupported_api"] == "ListResourcesByTags"


def test_alternative_scheme():
    alt = AlternativeScheme(
        unsupported_api="ListResourcesByTags",
        alternative_cli="hcloud ecs ListServers --filter-by-tags",
        feasibility=AlternativeFeasibility.PARTIAL,
        alternative_difference="No multi-tag support",
    )
    assert alt.feasibility == AlternativeFeasibility.PARTIAL


def test_analysis_config():
    config = AnalysisConfig(
        skills_repo_path="/path/to/skills",
        skill_names=["skill-a", "skill-b"],
    )
    d = asdict(config)
    assert d["skills_repo_path"] == "/path/to/skills"
    assert len(d["skill_names"]) == 2
    assert d["max_retries"] == 3


def test_sdk_analysis_result():
    result = SdkAnalysisResult(
        api_interfaces=[],
        sdk_calls=[],
        mapping_failures=["some_method"],
    )
    assert len(result.mapping_failures) == 1


def test_skill_analysis_result():
    skill_info = SkillImplResult(
        skill_name="test",
        implementation_type=ImplType.SDK,
        source_path="/path",
    )
    result = SkillAnalysisResult(skill_info=skill_info)
    assert result.analysis_status == AnalysisStatus.COMPLETED


def test_checkpoint_info():
    info = CheckpointInfo(
        thread_id="skill_test",
        skill_name="test",
        created_at="2024-01-01T00:00:00Z",
        last_step="impl_type_detection",
        status=StepStatus.COMPLETED,
        node_count=2,
    )
    assert info.node_count == 2