"""
    This module is responsible for redirect resolution and safety checks.
"""

# Standard Library Imports
import tldextract
import config

def is_suspicious_tld(tld: str) -> bool:
    """
    Check if the given TLD is in the list of suspicious TLDs.
    """
     
    if tld.lower() in config.SUSPICIOUS_TLDS:
        return True
    return False

def contains_suspicious_keyword(url: str) -> bool:
    """
    Check if the URL contains any suspicious keywords.
    """
    url_lower = url.lower()
    for keyword in config.SUSPICIOUS_KEYWORDS:
        if keyword in url_lower:
            return True
    return False

def is_url_shortened(url: str) -> bool:
    """
    Check if the URL is from a known URL shortener service.
    """
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    if domain.lower() in config.URL_SHORTENERS:
        return True
    return False