from os import getenv
from pathlib import Path

HAMCAM_PRODUCTION = getenv("HAMCAM_PRODUCTION")
SRC_DIR = Path(__file__).parents[1].resolve()
