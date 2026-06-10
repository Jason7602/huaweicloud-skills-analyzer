from src.analyzers.cli_coverage_analyzer import CliCoverageAnalyzer
from src.models.api_interface import ApiInterface, ApiParameter
from src.models.cli_command import CliCommand
from src.models.enums import CliCoveredStatus, HttpMethod


def _make_analyzer_with_commands(commands_dict):
    analyzer = CliCoverageAnalyzer(cli_tool_available=False, cli_tool_path="")
    analyzer._cli_commands = commands_dict
    return analyzer


def test_exact_coverage():
    cli_cmds = {
        "ecs": [CliCommand(
            cli_command="hcloud ecs CreateInstance",
            corresponding_api="CreateInstance",
            cli_service="ecs",
        )],
    }
    analyzer = _make_analyzer_with_commands(cli_cmds)
    api = ApiInterface(
        service_name="ecs",
        api_name="CreateInstance",
        api_path="/v1/cloudservers",
        http_method=HttpMethod.POST,
    )
    result = analyzer.analyze([api])
    assert result.coverage_map["CreateInstance"].is_covered == CliCoveredStatus.COVERED


def test_not_covered():
    cli_cmds = {
        "ecs": [CliCommand(
            cli_command="hcloud ecs ListServers",
            corresponding_api="ListServers",
            cli_service="ecs",
        )],
    }
    analyzer = _make_analyzer_with_commands(cli_cmds)
    api = ApiInterface(
        service_name="ecs",
        api_name="CreateInstance",
        api_path="/v1/cloudservers",
        http_method=HttpMethod.POST,
    )
    result = analyzer.analyze([api])
    assert result.coverage_map["CreateInstance"].is_covered == CliCoveredStatus.NOT_COVERED
    assert len(result.cli_gaps) > 0


def test_fuzzy_coverage():
    cli_cmds = {
        "ecs": [CliCommand(
            cli_command="hcloud ecs create_instance",
            corresponding_api="create_instance",
            cli_service="ecs",
        )],
    }
    analyzer = _make_analyzer_with_commands(cli_cmds)
    api = ApiInterface(
        service_name="ecs",
        api_name="CreateInstance",
        api_path="/v1/cloudservers",
        http_method=HttpMethod.POST,
    )
    result = analyzer.analyze([api])
    assert result.coverage_map["CreateInstance"].is_covered in (
        CliCoveredStatus.COVERED,
        CliCoveredStatus.UNCERTAIN,
    )


def test_gap_identification():
    cli_cmds = {}
    analyzer = _make_analyzer_with_commands(cli_cmds)
    api = ApiInterface(
        service_name="ecs",
        api_name="CreateInstance",
        api_path="/v1/cloudservers",
        http_method=HttpMethod.POST,
    )
    result = analyzer.analyze([api])
    assert len(result.cli_gaps) == 1
    assert result.cli_gaps[0].unsupported_api == "CreateInstance"


def test_alternative_search():
    cli_cmds = {
        "ecs": [CliCommand(
            cli_command="hcloud ecs ListServers",
            corresponding_api="ListServers",
            cli_service="ecs",
        )],
    }
    analyzer = _make_analyzer_with_commands(cli_cmds)
    api = ApiInterface(
        service_name="ecs",
        api_name="ListServersByTags",
        api_path="/v1/servers/tags",
        http_method=HttpMethod.GET,
    )
    result = analyzer.analyze([api])
    assert len(result.alternatives) > 0