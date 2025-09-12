import glob
import subprocess

import matplotlib.pyplot as plt
import pytest


# Disable plt.show() so scripts don't block tests
def no_op(*args, **kwargs):
    pass


# Collect all example scripts
example_scripts = glob.glob("docs/examples/ch*/solutions/diffpy-cmi/*.py")


@pytest.mark.parametrize("script_path", example_scripts)
def test_example_script(monkeypatch, script_path):
    """Run each example script and ensure it executes successfully."""
    # Patch plt.show to prevent GUI windows during tests
    monkeypatch.setattr(plt, "show", no_op)

    # Run the script as a subprocess
    result = subprocess.run(
        ["python", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Fail if return code is nonzero
    assert result.returncode == 0, (
        f"Script {script_path} failed.\n"
        f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
    )
