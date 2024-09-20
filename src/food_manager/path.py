from pathlib import Path

PACKAGE_PATH = Path(__file__).parent / ".package.bc"
DATA_PATH = PACKAGE_PATH / ".data"

WORLD_PATH = DATA_PATH / "world"
WEEKLY_DATA_PATH = DATA_PATH / "weekly"
CURRENT_WEEK_DATA_PATH = WEEKLY_DATA_PATH / "current"
CURRENT_WEEK_WORLD_PATH = CURRENT_WEEK_DATA_PATH / "world"
