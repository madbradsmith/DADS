"""D.A.D.S. (Deterministic Autonomous Decoupled State) Benchmark Suite.

Pre-registered empirical 11-turn workday benchmark evaluating multi-turn reliability,
state preservation, and context efficiency in autonomous AI systems.
"""

from pathlib import Path
import json

__version__ = "1.0.0"
__author__ = "Brad Smith / The Empire Architecture Squad"
__license__ = "Apache 2.0"

PROMPT_SET_SHA256 = "e66f70eafd7ce902813a99d7ba49a244e0abcf137cc70b6f6c4a5b248b985e8e"
PRE_REGISTERED_DATE = "2026-07-26"
TOTAL_EVALUATION_TURNS = 11000

DATA_DIR = Path(__file__).parent / "data"
PORTAL_DIR = Path(__file__).parent.parent / "portal"
DOCS_DIR = Path(__file__).parent.parent / "docs"


def load_benchmark_data() -> dict:
    """Load the canonical benchmark results and model receipts."""
    data_file = DATA_DIR / "data.json"
    if not data_file.exists():
        raise FileNotFoundError(f"Canonical benchmark data not found at {data_file}")
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_turns() -> list:
    """Load the 11 pre-registered standard trial turns."""
    turns_file = DATA_DIR / "turns_v1.json"
    if not turns_file.exists():
        raise FileNotFoundError(f"Turns definition not found at {turns_file}")
    with open(turns_file, "r", encoding="utf-8") as f:
        return json.load(f)

