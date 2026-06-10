import tempfile
from pathlib import Path

from src.analyzers.report_generator import ReportGenerator
from src.models.enums import (
    AnalysisStatus,
    CliCoveredStatus,
    CorrespondenceStatus,
    ImplType,
    ImpactLevel,
    IsMandatory,
    HttpMethod,
    ReplacementConclusion,
)
from src.models.api_interface import ApiInterface, OpenAPIUsage, SourceSdkCall, ApiBusinessRole
from src.models.cli_gap import CliGap
from src.models.cli_command import KooCliCorrespondence, KooCliCommand, EffectEquivalenceResult
from src.models.replacement import KooCliReplacementFeasibility, BlockingPoint
from src.models.report import (
    CliCoverageResult,
    CliCorrespondenceResult,
    ReportStageResult,
    SkillAnalysisResult,
    SdkAnalysisResult,
)
from src.models.skill import SkillImplResult


def _make_skill_result():
    openapi_usage = OpenAPIUsage(
        usage_id="ecs-create-1",
        service_name="ECS",
        api_name="CreateInstance",
        api_path="/v1/cloudservers",
        http_method=HttpMethod.POST,
        source_sdk_call=SourceSdkCall(
            service_name="ecs",
            client_class="EcsClient",
            method_name="create_instance",
            source_file="skill.py",
            line_number=42,
        ),
        business_role=ApiBusinessRole(
            usage_id="ecs-create-1",
            business_role="创建云服务器",
            is_mandatory=IsMandatory.MANDATORY,
        ),
    )

    correspondence = KooCliCorrespondence(
        usage_id="ecs-create-1",
        api_name="CreateInstance",
        service_name="ECS",
        selected_command=KooCliCommand(
            command="hcloud ecs create-instance",
            service_name="ECS",
            operation_name="create",
            resource_object="instance",
        ),
        status=CorrespondenceStatus.EXACT,
        difference_description="",
        impact_description="",
    )

    feasibility = KooCliReplacementFeasibility(
        conclusion=ReplacementConclusion.FULLY_REPLACEABLE,
        reason="所有必须接口均存在效果完全一致的KooCLI命令",
        replaceable_scope=["CreateInstance"],
    )

    return SkillAnalysisResult(
        skill_info=SkillImplResult(
            skill_name="test-skill",
            implementation_type=ImplType.SDK,
            source_path="/path/to/skill",
            business_goal="Test business goal",
            sdk_evidence=["from huaweicloudsdkecs"],
        ),
        sdk_result=SdkAnalysisResult(
            api_interfaces=[ApiInterface(
                service_name="ECS",
                api_name="CreateInstance",
                api_path="/v1/cloudservers",
                http_method=HttpMethod.POST,
            )],
            openapi_usages=[openapi_usage],
            api_business_roles=[openapi_usage.business_role],
            stage_1_result=ReportStageResult(
                stage_name="第一阶段",
                summary="识别到1个Open API接口，1个必须接口。",
            ),
        ),
        correspondence_result=CliCorrespondenceResult(
            correspondences=[correspondence],
            incomplete_apis=[],
            info_source="local_cli",
            stage_2_result=ReportStageResult(
                stage_name="第二阶段",
                summary="1个接口效果完全一致，0个不完全一致。",
            ),
        ),
        replacement_feasibility=feasibility,
        stage_3_result=ReportStageResult(
            stage_name="第三阶段",
            summary="可以完全替换为KooCLI实现。",
        ),
    )


def test_report_generation():
    with tempfile.TemporaryDirectory() as tmp:
        generator = ReportGenerator(output_dir=tmp)
        result = _make_skill_result()
        output = generator.generate(result)

        assert "test-skill" in output.content_md
        assert "ECS" in output.content_md
        assert "CreateInstance" in output.content_md
        assert output.file_path.endswith(".md")


def test_report_has_all_sections():
    with tempfile.TemporaryDirectory() as tmp:
        generator = ReportGenerator(output_dir=tmp)
        result = _make_skill_result()
        output = generator.generate(result)

        assert "基本信息" in output.content_md
        assert "第一阶段" in output.content_md
        assert "Open API" in output.content_md
        assert "第二阶段" in output.content_md
        assert "KooCLI" in output.content_md
        assert "第三阶段" in output.content_md
        assert "最终结论" in output.content_md


def test_report_has_replacement_conclusion():
    with tempfile.TemporaryDirectory() as tmp:
        generator = ReportGenerator(output_dir=tmp)
        result = _make_skill_result()
        output = generator.generate(result)

        assert "可以完全替换" in output.content_md


def test_report_desensitization():
    content = "ak=AKILOSSEUSSEXAMPLE\npassword=MySecret123"
    result = ReportGenerator._desensitize(content)
    assert "AKILOSSEUSSEXAMPLE" not in result
    assert "MySecret123" not in result
    assert "[REDACTED]" in result
