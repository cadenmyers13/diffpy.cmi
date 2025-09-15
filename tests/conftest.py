import importlib.util
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

__examples_dir__ = Path(__file__).parent.parent / "docs" / "examples"


@pytest.fixture
def user_filesystem(tmp_path):
    base_dir = Path(tmp_path)
    home_dir = base_dir / "home_dir"
    home_dir.mkdir(parents=True, exist_ok=True)
    cwd_dir = base_dir / "cwd_dir"
    cwd_dir.mkdir(parents=True, exist_ok=True)

    home_config_data = {"username": "home_username", "email": "home@email.com"}
    with open(home_dir / "diffpyconfig.json", "w") as f:
        json.dump(home_config_data, f)

    yield tmp_path


def load_module_from_path(path: Path):
    """Load a module given an absolute Path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def suppress_plots(monkeypatch):
    """Fixture to suppress plt.show during tests."""
    monkeypatch.setattr(plt, "show", lambda *a, **k: None)


def run_cmi_script(script_path: Path, suppress_plots):
    """General runner for example scripts with a main()."""
    module = load_module_from_path(script_path)
    assert hasattr(module, "main"), f"{script_path} has no main() function"
    module.main()
