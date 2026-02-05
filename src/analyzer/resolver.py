"""
    This module is responsible for redirect resolution and safety checks.
"""

# Standard Library Imports
import logging
from urllib.parse import urlparse, urljoin

# Analyzer Imports (Internal)
import normalize 