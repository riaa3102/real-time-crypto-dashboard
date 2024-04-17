from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Directory paths
LOGS_DIR = BASE_DIR / "logs"


def create_dirs():
    """Create necessary directories if they don't exist."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


create_dirs()

