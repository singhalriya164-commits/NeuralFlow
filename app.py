"""
NEURALFLOW — Enterprise Machine Learning Platform Root Launcher
================================================================
Executes backend/app.py while ensuring correct working directory,
module paths, and environment settings.
"""

import os
import sys
import runpy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
BACKEND_APP = os.path.join(BACKEND_DIR, "app.py")

if __name__ == "__main__":
    os.chdir(BACKEND_DIR)
    if BACKEND_DIR not in sys.path:
        sys.path.insert(0, BACKEND_DIR)
    runpy.run_path(BACKEND_APP, run_name="__main__")
