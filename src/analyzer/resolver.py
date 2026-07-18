"""
This module is responsible for redirect resolution and safety checks.

rewrote entire code for better error handling and added functions to check for suspicious TLDs,
keywords, and URL shorteners.


"""

# Library imports
import requests
import tldextract
from urllib.parse import urlparse

# Local imports
import config 


def get_url_parts(url: str) -> dict:
    """
    parse and return reusable URL parts for analyzer modules.
    """
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    tld = hostname.split('.')[-1] if '.' in hostname else ''
    extracted = tldextract.extract(url)
    registered_domain = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain

    return {
        "scheme": parsed.scheme.lower(),
        "hostname": hostname.lower(),
        "tld": tld.lower(),
        "registered_domain": registered_domain.lower()
    }


def analyze_url_signals(url: str) -> dict:
    """
    evaluate reusable URL-level risk signals in a single pass.
    """
    parts = get_url_parts(url)
    url_lower = url.lower()

    return {
        "parts": parts,
        "suspicious_tld": parts["tld"] in config.SUSPICIOUS_TLDS,
        "suspicious_keyword": any(keyword in url_lower for keyword in config.SUSPICIOUS_KEYWORDS),
        "shortener_domain": parts["registered_domain"] in config.URL_SHORTENERS,
        "uses_https": parts["scheme"] == "https",
        "has_punycode": 'xn--' in parts["hostname"],
    }

def get_final_url(url: str) -> dict:
    """
    follow redirect safely in config.
    """
    chain = []
    headers = {'User-Agent': config.USER_AGENT}

    try:
        # prevent hanging
        response = requests.head(
            url, 
            allow_redirects=True, 
            timeout=config.REQUEST_TIMEOUT, 
            headers=headers
        )
        
        # track redirect 
        if response.history:
            for resp in response.history:
                chain.append(resp.url)
        
        return {
            "original_url": url,
            "final_url": response.url,
            "chain": chain,
            "status_code": response.status_code,
            "error": None
        }

    except requests.Timeout:
        return {"error": "Timeout reached", "final_url": url, "chain": chain}
    except Exception as e:
        return {"error": str(e), "final_url": url, "chain": chain}

def is_suspicious_tld(tld: str) -> bool:
    """
    check if there are any suspicious tlds
    """
    return tld.lower() in config.SUSPICIOUS_TLDS

def contains_suspicious_keyword(url: str) -> bool:
    """
    check if there contains any suspicious keywords.
    """
    url_lower = url.lower()
    return any(keyword in url_lower for keyword in config.SUSPICIOUS_KEYWORDS)

def is_url_shortened(url: str) -> bool:
    """
    check if URL is shortened
    """
    try:
        parts = get_url_parts(url)
        return parts["registered_domain"] in config.URL_SHORTENERS
    except Exception:
        return False
    
def uses_https(url: str) -> bool:
    """
    check if URL uses HTTPS.
    """
    parts = get_url_parts(url)
    return parts["scheme"] == "https"

def has_punycode(url: str) -> bool:
    """
    check if hostname contains punycode marker.
    """
    parts = get_url_parts(url)
    return 'xn--' in parts["hostname"]