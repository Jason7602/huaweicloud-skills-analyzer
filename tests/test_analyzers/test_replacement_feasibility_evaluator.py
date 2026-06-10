import pytest

from src.analyzers.replacement_feasibility_evaluator import ReplacementFeasibilityEvaluator
from src.models.api_interface import ApiBusinessRole, OpenAPIUsage, SourceSdkCall
from src.models.cli_command import KooCliCorrespondence
from src.models.enums import CorrespondenceStatus, HttpMethod, IsMandatory, ReplacementConclusion


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


def _make_correspondence(status=CorrespondenceStatus.EXACT, usage_id="ecs-1", api_name="CreateInstance") -> KooCliCorrespondence:
    return KooCliCorrespondence(
        usage_id=usage_id,
        api_name=api_name,
        service_name="ECS",
        status=status,
    )


@pytest.fixture
def evaluator():
    return ReplacementFeasibilityEvaluator()


class TestFullyReplaceable:
    def test_all_exact_gives_fully_replaceable(self, evaluator):
        usages = [_make_usage()]
        roles = [_make_role()]
        corrs = [_make_correspondence()]
        feasibility, stage_3 = evaluator.evaluate(usages, roles, corrs)
        assert feasibility.conclusion == ReplacementConclusion.FULLY_REPLACEABLE

    def test_replaceable_scope_populated(self, evaluator):
        usages = [_make_usage()]
        roles = [_make_role()]
        corrs = [_make_correspondence()]
        feasibility, _ = evaluator.evaluate(usages, roles, corrs)
        assert "CreateInstance" in feasibility.replaceable_scope

    def test_no_blocking_points(self, evaluator):
        usages = [_make_usage()]
        roles = [_make_role()]
        corrs = [_make_correspondence()]
        feasibility, _ = evaluator.evaluate(usages, roles, corrs)
        assert len(feasibility.blocking_points) == 0


class TestNotReplaceable:
    def test_mandatory_none_gives_not_replaceable(self, evaluator):
        usages = [_make_usage()]
        roles = [_make_role()]
        corrs = [_make_correspondence(status=CorrespondenceStatus.NONE)]
        feasibility, _ = evaluator.evaluate(usages, roles, corrs)
        assert feasibility.conclusion == ReplacementConclusion.NOT_REPLACEABLE

    def test_has_blocking_points(self, evaluator):
        usages = [_make_usage()]
        roles = [_make_role()]
        corrs = [_make_correspondence(status=CorrespondenceStatus.NONE)]
        feasibility, _ = evaluator.evaluate(usages, roles, corrs)
        assert len(feasibility.blocking_points) > 0


class TestNeedsConfirmation:
    def test_empty_usages_gives_needs_confirmation(self, evaluator):
        feasibility, _ = evaluator.evaluate([], [], [])
        assert feasibility.conclusion == ReplacementConclusion.NEEDS_CONFIRMATION


class TestPartiallyReplaceable:
    def test_optional_none_gives_partially_replaceable(self, evaluator):
        usages = [_make_usage()]
        roles = [_make_role(is_mandatory=IsMandatory.OPTIONAL)]
        corrs = [_make_correspondence(status=CorrespondenceStatus.NONE)]
        feasibility, _ = evaluator.evaluate(usages, roles, corrs)
        assert feasibility.conclusion == ReplacementConclusion.PARTIALLY_REPLACEABLE


class TestStatistics:
    def test_statistics_populated(self, evaluator):
        usages = [_make_usage()]
        roles = [_make_role()]
        corrs = [_make_correspondence()]
        feasibility, _ = evaluator.evaluate(usages, roles, corrs)
        assert feasibility.statistics["total"] == 1
        assert feasibility.statistics["has_correspondence"] == 1

    def test_mixed_statistics(self, evaluator):
        usages = [
            _make_usage(usage_id="1", api_name="CreateInstance"),
            _make_usage(usage_id="2", api_name="ListInstances"),
        ]
        roles = [
            _make_role(usage_id="1"),
            _make_role(usage_id="2", is_mandatory=IsMandatory.OPTIONAL),
        ]
        corrs = [
            _make_correspondence(usage_id="1", api_name="CreateInstance", status=CorrespondenceStatus.EXACT),
            _make_correspondence(usage_id="2", api_name="ListInstances", status=CorrespondenceStatus.NONE),
        ]
        feasibility, _ = evaluator.evaluate(usages, roles, corrs)
        assert feasibility.statistics["total"] == 2
        assert feasibility.statistics["has_correspondence"] == 1
        assert feasibility.statistics["no_correspondence"] == 1


class TestStage3Result:
    def test_stage_3_result_generated(self, evaluator):
        usages = [_make_usage()]
        roles = [_make_role()]
        corrs = [_make_correspondence()]
        feasibility, stage_3 = evaluator.evaluate(usages, roles, corrs)
        assert stage_3 is not None
        assert "第三阶段" in stage_3.stage_name
        assert stage_3.summary != ""
