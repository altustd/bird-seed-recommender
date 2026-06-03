"""
Streamlit Cloud entry point wrapper.

This file exists purely for convenience with Streamlit Community Cloud
deployments, which sometimes default to looking for `streamlit_app.py`.

It simply executes the real app (app.py) so we keep a single source of truth
and our local `pixi run app` / other tooling continues to use the standard `app.py`.

Do not put new logic here.
"""

from pathlib import Path
import runpy

# Run the original app.py as if it were the main script.
# This preserves all top-level Streamlit calls, state, etc.
app_path = Path(__file__).parent / "app.py"
runpy.run_path(str(app_path), run_name="__main__")
