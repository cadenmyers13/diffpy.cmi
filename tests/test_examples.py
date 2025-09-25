import os
import runpy


def test_all_examples(tmp_examples):
    """Run all or selected example scripts depending on FAST_EXAMPLES
    var in CI."""
    scripts = list(tmp_examples.rglob("**/solutions/diffpy-cmi/*.py"))
    # sort so fitBulkNi.py runs first
    scripts.sort(key=lambda s: 0 if s.name == "fitBulkNi.py" else 1)
    # FAST_EXAMPLES=1 -> only run fitBulkNi.py
    if os.getenv("FAST_EXAMPLES") == "1":
        scripts = [s for s in scripts if s.name == "fitBulkNi.py"]
    for script in scripts:
        print(f"Testing {script}")
        runpy.run_path(str(script), run_name="__main__")
