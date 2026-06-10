import pytest

from src.analyzers.cli_correspondence_analyzer import CliCorrespondenceAnalyzer
from src.models.api_interface import ApiBusinessRole, OpenAPIUsage, SourceSdkCall
from src.models.enums import CorrespondenceStatus, HttpMethod, IsMandatory


def _make_usage(**overrides) -> OpenAPIUsage:
    defaults = dict(
        usage_id="ecs-1",
        service_name="ECS",
        api_name="CreateInstance",
        api_path="/v1/cloudservers",
        http_method=HttpMethod.POST,
        source_sdk_call=SourceSdkCall("ecs", "EcsClient", "create_instance"),
    )
    defaults.update(overrides)
    return OpenAPIUsage(**defaults)


def _make_role(**overrides) -> ApiBusinessRole:
    defaults = dict(
        usage_id="ecs-1",
        business_role="创建云服务器",
        is_mandatory=IsMandatory.MANDATORY,
    )
    defaults.update(overrides)
    return ApiBusinessRole(**defaults)


@pytest.fixture
def analyzer():
    return CliCorrespondenceAnalyzer(cli_tool_available=False)


class TestNoCliTool:
    def test_no_cli_tool_gives_none_status(self, analyzer):
        usages = [_make_usage()]
        roles = [_make_role()]
        result = analyzer.analyze(usages, roles)
        assert len(result.correspondences) == 1
        assert result.correspondences[0].status == CorrespondenceStatus.NONE

    def test_incomplete_apis_listed(self, analyzer):
        usages = [_make_usage()]
        roles = [_make_role()]
        result = analyzer.analyze(usages, roles)
        assert "CreateInstance" in result.incomplete_apis

    def test_info_source_is_none(self, analyzer):
        usages = [_make_usage()]
        result = analyzer.analyze(usages, [])
        assert result.info_source == "none"

    def test_stage_2_result_generated(self, analyzer):
        usages = [_make_usage()]
        roles = [_make_role()]
        result = analyzer.analyze(usages, roles)
        assert result.stage_2_result is not None
        assert "第二阶段" in result.stage_2_result.stage_name


class TestMultipleUsages:
    def test_multiple_usages(self, analyzer):
        usages = [
            _make_usage(usage_id="ecs-1", api_name="CreateInstance"),
            _make_usage(usage_id="ecs-2", api_name="ListInstances", api_path="/v1/cloudservers/detail", http_method=HttpMethod.GET),
        ]
        roles = [
            _make_role(usage_id="ecs-1", business_role="创建云服务器"),
            _make_role(usage_id="ecs-2", business_role="查询云服务器列表"),
        ]
        result = analyzer.analyze(usages, roles)
        assert len(result.correspondences) == 2


    def test_empty_usages(self, analyzer):
        result = analyzer.analyze([], [])
        assert len(result.correspondences) == 0
        assert len(result.incomplete_apis) == 0