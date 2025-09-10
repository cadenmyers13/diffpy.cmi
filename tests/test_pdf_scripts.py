import glob
import subprocess

import matplotlib.pyplot as plt
import pytest


# A no-op function to replace plt.show() during tests
def no_op(*args, **kwargs):
    pass


# Decorator to mark this as a pytest function and provide parameters
@pytest.mark.parametrize(
    "script_path", glob.glob("docs/examples/ch*/solutions/diffpy-cmi/*.py")
)
def test_script_execution(monkeypatch, script_path):
    """Test execution of each script while suppressing plot display."""
    # Patch plt.show to suppress plot display
    monkeypatch.setattr(plt, "show", no_op)

    # Run the script
    result = subprocess.run(
        ["python", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Ensure the script runs successfully
    assert (
        result.returncode == 0
    ), f"Script {script_path} failed with error: {result.stderr}"
