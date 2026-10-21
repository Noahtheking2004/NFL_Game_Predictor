from pathlib import Path

# Project root = two folders up from this file (SRC/Py -> SRC -> PythonProject)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = str(PROJECT_ROOT / "nfl.db")

