from src.graph.routes import route_by_impl_type
from src.models.enums import ImplType


def test_route_always_goes_to_sdk_analysis():
    for impl_type in [ImplType.KOOCLI.value, "KooCLI", ImplType.SDK.value, ImplType.HYBRID.value, ImplType.UNKNOWN.value]:
        state = {"implementation_type": impl_type}
        assert route_by_impl_type(state) == "sdk_interface_analysis"
