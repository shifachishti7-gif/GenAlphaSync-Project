# conftest.py

import sys
from pathlib import Path

# Get the path to the project root (where this file is located)
project_root = str(Path(__file__).parent)

# Add the project root to the system path
# This allows pytest to find 'main.py' and 'app.*' modules
sys.path.append(project_root)