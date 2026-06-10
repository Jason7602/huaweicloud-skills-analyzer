import pytest

from src.nodes.report_gen_node import (
    _dict_to_api_business_role,
    _dict_to_api_parameter,
    _dict_to_blocking_point,
    _dict_to_effect_equivalence_result,
    _dict_to_equivalence_dimension_result,
    _dict_to_koocli_command,
    _dict_to_koocli_correspondence,
    _dict_to_koocli_parameter,
    _dict_to_openapi_usage,
    _dict_to_replacement_feasibility,
    _dict_to_report_stage_result,
    _dict_to_source_sdk_call,
    _safe_enum,
)
from src.models.enums import (
    Acceptability,
    CliInfoSource,
    CorrespondenceStatus,
    DimensionStatus,
    HttpMethod,
    IsMandatory,
    LlmEnhancementStatus,
    ReplacementConclusion,
)


class TestSafeEnum:
    def test_valid_value(self):
        assert _safe_enum(HttpMethod, "POST") == HttpMethod.POST

    def test_already_enum(self):
        assert _safe_enum(HttpMethod, HttpMethod.GET) == HttpMethod.GET

    def test_invalid_value_returns_default(self):
        assert _safe_enum(HttpMethod, "INVALID", HttpMethod.GET) == HttpMethod.GET

    def test_none_returns_default(self):
        assert _safe_enum(HttpMethod, None, HttpMethod.GET) == HttpMethod.GET


class TestDictToApiParameter:
    def test_full_dict(self):
        d = {"name": "flavor", "param_type": "str", "is_required": True, "description": "规格"}
        p = _dict_to_api_parameter(d)
        assert p.name == "flavor"
        assert p.is_required is True

    def test_missing_fields(self):
        p = _dict_to_api_parameter({})
        assert p.name == ""
        assert p.is_required is False


class TestDictToSourceSdkCall:
    def test_full_dict(self):
        d = {"service_name": "ecs", "client_class": "EcsClient", "method_name": "create", "source_file": "a.py", "line_number": 10}
        r = _dict_to_source_sdk_call(d)
        assert r.service_name == "ecs"
        assert r.line_number == 10

    def test_none_returns_default(self):
        r = _dict_to_source_sdk_call(None)
        assert r.service_name == ""


class TestDictToApiBusinessRole:
    def test_full_dict(self):
        d = {"usage_id": "1", "business_role": "创建", "is_mandatory": "mandatory"}
        r = _dict_to_api_business_role(d)
        assert r.usage_id == "1"
        assert r.is_mandatory == IsMandatory.MANDATORY

    def test_none_returns_none(self):
        assert _dict_to_api_business_role(None) is None


class TestDictToOpenApiUsage:
    def test_full_dict(self):
        d = {
            "usage_id": "1",
            "service_name": "ECS",
            "api_name": "CreateInstance",
            "api_path": "/v1/cloudservers",
            "http_method": "POST",
            "actual_params": {"name": "test"},
            "source_sdk_call": {"service_name": "ecs", "client_class": "EcsClient", "method_name": "create"},
            "business_role": {"usage_id": "1", "business_role": "创建", "is_mandatory": "mandatory"},
        }
        r = _dict_to_openapi_usage(d)
        assert r.service_name == "ECS"
        assert r.http_method == HttpMethod.POST
        assert r.source_sdk_call.client_class == "EcsClient"
        assert r.business_role.is_mandatory == IsMandatory.MANDATORY

    def test_minimal_dict(self):
        d = {"usage_id": "1", "service_name": "ECS", "api_name": "List", "api_path": "/", "http_method": "GET"}
        r = _dict_to_openapi_usage(d)
        assert r.service_name == "ECS"


class TestDictToKooCliCommand:
    def test_full_dict(self):
        d = {"command": "hcloud ecs create", "service_name": "ECS", "operation_name": "create", "info_source": "local_cli"}
        r = _dict_to_koocli_command(d)
        assert r.command == "hcloud ecs create"
        assert r.info_source == CliInfoSource.LOCAL_CLI

    def test_none_returns_none(self):
        assert _dict_to_koocli_command(None) is None


class TestDictToEffectEquivalenceResult:
    def test_full_dict(self):
        d = {
            "usage_id": "1",
            "api_name": "Create",
            "candidate_command": None,
            "overall_status": "效果完全一致",
            "confidence": 0.9,
            "acceptable": "可接受",
        }
        r = _dict_to_effect_equivalence_result(d)
        assert r.overall_status == CorrespondenceStatus.EXACT
        assert r.acceptable == Acceptability.ACCEPTABLE


class TestDictToKooCliCorrespondence:
    def test_full_dict(self):
        d = {
            "usage_id": "1",
            "api_name": "Create",
            "service_name": "ECS",
            "status": "效果完全一致",
            "info_source": "local_cli",
            "acceptable": "可接受",
        }
        r = _dict_to_koocli_correspondence(d)
        assert r.status == CorrespondenceStatus.EXACT
        assert r.info_source == CliInfoSource.LOCAL_CLI


class TestDictToReplacementFeasibility:
    def test_full_dict(self):
        d = {
            "conclusion": "可以完全替换",
            "reason": "all exact",
            "blocking_points": [],
            "replaceable_scope": ["Create"],
            "non_replaceable_scope": [],
            "statistics": {"total": 1},
            "llm_status": "未启用",
        }
        r = _dict_to_replacement_feasibility(d)
        assert r.conclusion == ReplacementConclusion.FULLY_REPLACEABLE
        assert "Create" in r.replaceable_scope

    def test_none_returns_none(self):
        assert _dict_to_replacement_feasibility(None) is None


class TestDictToReportStageResult:
    def test_full_dict(self):
        d = {"stage_name": "第一阶段", "summary": "1个接口", "details": {}, "warnings": []}
        r = _dict_to_report_stage_result(d)
        assert r.stage_name == "第一阶段"

    def test_none_returns_none(self):
        assert _dict_to_report_stage_result(None) is None