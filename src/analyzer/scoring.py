"""
Handles scoring of URLs based on various criteria.
"""

# imports analyzer modules

import analyzer.resolver as resolver
from urllib.parse import urlparse

#main scoring function

def score_url(url: str, number: int) -> int:
    """
    Scores the given URL based on various risk factors.
    Returns an integer score; higher means more risky.
    """

    # for debug
    print(f"Scanning: {url}, Index: {number}")

    score = 0

    # Check for suspicious TLDs
    extracted = urlparse(url)
    hostname = extracted.hostname or ""
    tld = hostname.split('.')[-1] if '.' in hostname else ''
    if resolver.is_suspicious_tld(tld):
        score += 30  # high risk for suspicious TLDs

    # Check for suspicious keywords
    if resolver.contains_suspicious_keyword(url):
        score += 20  # moderate risk for suspicious keywords

    # Check if URL is shortened
    if resolver.is_url_shortened(url):
        score += 10  # low risk for shortened URLs

    return score