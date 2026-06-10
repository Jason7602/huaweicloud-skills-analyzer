import tempfile
from pathlib import Path

from src.analyzers.impl_type_detector import ImplTypeDetector
from src.models.enums import ImplType


def _create_skill_dir(tmp_dir: str, name: str, files: dict) -> Path:
    skill_path = Path(tmp_dir) / name
    skill_path.mkdir(parents=True, exist_ok=True)
    for filename, content in files.items():
        (skill_path / filename).parent.mkdir(parents=True, exist_ok=True)
        (skill_path / filename).write_text(content, encoding="utf-8")
    return skill_path


def test_detect_sdk_only():
    with tempfile.TemporaryDirectory() as tmp:
        _create_skill_dir(tmp, "sdk-skill", {
            "main.py": "from huaweicloudsdkecs.v2 import EcsClient\nclient = EcsClient()\nclient.create_instance(req)",
        })
        detector = ImplTypeDetector()
        result = detector.detect(str(Path(tmp) / "sdk-skill"))
        assert result.implementation_type == ImplType.SDK
        assert len(result.sdk_evidence) > 0


def test_detect_cli_only():
    with tempfile.TemporaryDirectory() as tmp:
        _create_skill_dir(tmp, "cli-skill", {
            "main.py": "import subprocess\nsubprocess.run(['hcloud', 'ecs', 'ListServers'])",
        })
        detector = ImplTypeDetector()
        result = detector.detect(str(Path(tmp) / "cli-skill"))
        assert result.implementation_type == ImplType.KOOCLI
        assert len(result.cli_evidence) > 0


def test_detect_hybrid():
    with tempfile.TemporaryDirectory() as tmp:
        _create_skill_dir(tmp, "hybrid-skill", {
            "main.py": "from huaweicloudsdkecs.v2 import EcsClient\nimport subprocess\nsubprocess.run(['hcloud', 'ecs', 'ListServers'])\nclient = EcsClient()",
        })
        detector = ImplTypeDetector()
        result = detector.detect(str(Path(tmp) / "hybrid-skill"))
        assert result.implementation_type == ImplType.HYBRID
        assert len(result.cli_evidence) > 0
        assert len(result.sdk_evidence) > 0


def test_detect_unknown():
    with tempfile.TemporaryDirectory() as tmp:
        _create_skill_dir(tmp, "unknown-skill", {
            "main.py": "print('hello world')",
        })
        detector = ImplTypeDetector()
        result = detector.detect(str(Path(tmp) / "unknown-skill"))
        assert result.implementation_type == ImplType.UNKNOWN


def test_detect_cli_in_shell_script():
    with tempfile.TemporaryDirectory() as tmp:
        _create_skill_dir(tmp, "shell-skill", {
            "run.sh": "#!/bin/bash\nhcloud ecs ListServers",
        })
        detector = ImplTypeDetector()
        result = detector.detect(str(Path(tmp) / "shell-skill"))
        assert result.implementation_type == ImplType.KOOCLI
        assert len(result.cli_evidence) > 0


def test_business_goal_from_readme():
    with tempfile.TemporaryDirectory() as tmp:
        _create_skill_dir(tmp, "readme-skill", {
            "README.md": "# My Skill\n\nThis skill manages ECS instances.\n\n## Details",
            "main.py": "pass",
        })
        detector = ImplTypeDetector()
        result = detector.detect(str(Path(tmp) / "readme-skill"))
        assert "ECS" in result.business_goal