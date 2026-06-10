import pytest

from src.analyzers.effect_equivalence_evaluator import EffectEquivalenceEvaluator
from src.models.api_interface import ApiBusinessRole, ApiParameter, OpenAPIUsage, SourceSdkCall
from src.models.cli_command import EffectEquivalenceResult, KooCliCommand, KooCliParameter
from src.models.enums import (
    Acceptability,
    CorrespondenceStatus,
    DimensionStatus,
    HttpMethod,
    IsMandatory,
)


def _make_usage(**overrides) -> OpenAPIUsage:
    defaults = dict(
        usage_id="test-1",
        service_name="ECS",
        api_name="CreateInstance",
        api_path="/v1/instances",
        http_method=HttpMethod.POST,
        actual_params={"name": "test", "flavor": "s6.small.1"},
        source_sdk_call=SourceSdkCall("ecs", "EcsClient", "create_instance"),
    )
    defaults.update(overrides)
    return OpenAPIUsage(**defaults)


def _make_command(**overrides) -> KooCliCommand:
    defaults = dict(
        command="hcloud ecs create-instance",
        service_name="ECS",
        operation_name="createInstance",
        resource_object="instance",
        parameters=[
            KooCliParameter(name="name", required=True),
            KooCliParameter(name="flavor", required=True),
        ],
    )
    defaults.update(overrides)
    return KooCliCommand(**defaults)


def _make_role(**overrides) -> ApiBusinessRole:
    defaults = dict(
        usage_id="test-1",
        business_role="创建云服务器",
        is_mandatory=IsMandatory.MANDATORY,
    )
    defaults.update(overrides)
    return ApiBusinessRole(**defaults)


@pytest.fixture
def evaluator():
    return EffectEquivalenceEvaluator()


class TestNoCandidateCommand:
    def test_overall_status_is_none(self, evaluator):
        usage = _make_usage()
        result = evaluator.evaluate(usage, None, None)
        assert result.overall_status == CorrespondenceStatus.NONE

    def test_all_dimensions_not_satisfied(self, evaluator):
        usage = _make_usage()
        result = evaluator.evaluate(usage, None, None)
        assert all(d.status == DimensionStatus.NOT_SATISFIED for d in result.dimensions)

    def test_not_acceptable(self, evaluator):
        usage = _make_usage()
        result = evaluator.evaluate(usage, None, None)
        assert result.acceptable == Acceptability.NOT_ACCEPTABLE

    def test_seven_dimensions(self, evaluator):
        usage = _make_usage()
        result = evaluator.evaluate(usage, None, None)
        assert len(result.dimensions) == 7


class TestExactEquivalence:
    def test_all_satisfied_gives_exact(self, evaluator):
        usage = _make_usage()
        cmd = _make_command()
        role = _make_role(state_impact="创建云服务器资源")
        result = evaluator.evaluate(usage, role, cmd)
        assert result.overall_status == CorrespondenceStatus.EXACT

    def test_acceptable_when_exact(self, evaluator):
        usage = _make_usage()
        cmd = _make_command()
        role = _make_role(state_impact="创建云服务器资源")
        result = evaluator.evaluate(usage, role, cmd)
        assert result.acceptable == Acceptability.ACCEPTABLE


class TestServiceMismatch:
    def test_service_mismatch_gives_partial(self, evaluator):
        usage = _make_usage()
        cmd = _make_command(service_name="VPC")
        result = evaluator.evaluate(usage, None, cmd)
        assert result.overall_status == CorrespondenceStatus.PARTIAL

    def test_service_dimension_not_satisfied(self, evaluator):
        usage = _make_usage()
        cmd = _make_command(service_name="VPC")
        result = evaluator.evaluate(usage, None, cmd)
        svc_dim = next(d for d in result.dimensions if d.dimension_name == "目标服务一致")
        assert svc_dim.status == DimensionStatus.NOT_SATISFIED


class TestParameterMissing:
    def test_missing_param_gives_partial(self, evaluator):
        usage = _make_usage(actual_params={"name": "test", "flavor": "s6.small.1", "image": "centos7"})
        cmd = _make_command(parameters=[KooCliParameter(name="name"), KooCliParameter(name="flavor")])
        result = evaluator.evaluate(usage, None, cmd)
        param_dim = next(d for d in result.dimensions if d.dimension_name == "参数表达完整")
        assert param_dim.status == DimensionStatus.NOT_SATISFIED


class TestOverallStatusRules:
    def test_any_not_satisfied_gives_partial(self, evaluator):
        usage = _make_usage()
        cmd = _make_command(service_name="VPC")
        result = evaluator.evaluate(usage, None, cmd)
        assert result.overall_status == CorrespondenceStatus.PARTIAL

    def test_all_satisfied_gives_exact(self, evaluator):
        usage = _make_usage()
        cmd = _make_command()
        role = _make_role(state_impact="创建资源")
        result = evaluator.evaluate(usage, role, cmd)
        assert result.overall_status == CorrespondenceStatus.EXACT

    def test_no_failed_but_unknown_gives_unknown(self, evaluator):
        usage = _make_usage(response_fields_used=["job_id"])
        cmd = _make_command(output_fields=[])
        result = evaluator.evaluate(usage, None, cmd)
        assert result.overall_status == CorrespondenceStatus.UNKNOWN


class TestConfidence:
    def test_exact_has_high_confidence(self, evaluator):
        usage = _make_usage()
        cmd = _make_command()
        role = _make_role(state_impact="创建资源")
        result = evaluator.evaluate(usage, role, cmd)
        assert result.confidence >= 0.8

    def test_none_has_full_confidence(self, evaluator):
        usage = _make_usage()
        result = evaluator.evaluate(usage, None, None)
        assert result.confidence == 1.0
