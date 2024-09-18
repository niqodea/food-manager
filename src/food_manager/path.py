from pathlib import Path

PACKAGE_PATH = Path(__file__).parent / ".package.bc"
DATA_PATH = PACKAGE_PATH / ".data"

BALLOONS_PATH = DATA_PATH / "balloons"
WEEKLY_DATA_PATH = DATA_PATH / "weekly"
CURRENT_WEEK_DATA_PATH = WEEKLY_DATA_PATH / "current"
CURRENT_WEEK_BALLOONS_PATH = CURRENT_WEEK_DATA_PATH / "balloons"
