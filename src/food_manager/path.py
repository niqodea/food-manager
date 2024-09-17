from pathlib import Path

PACKAGE_PATH = Path(__file__).parent / ".package.bc"
DATA_PATH = PACKAGE_PATH / ".data"

GLOBAL_DATABASE_PATH = DATA_PATH / "global"
WEEKLY_DATABASES_PATH = DATA_PATH / "weekly"
CURRENT_WEEKLY_DATABASE_PATH = WEEKLY_DATABASES_PATH / "current"
