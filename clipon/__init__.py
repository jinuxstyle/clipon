import sys
import os
"""
Add current directory to python library searching path.
It's for fixing ImportError when using installed clipon.
"""
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
