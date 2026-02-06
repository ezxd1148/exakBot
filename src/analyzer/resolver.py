"""
This module is responsible for redirect resolution and safety checks.

rewrote entire code for better error handling and added functions to check for suspicious TLDs,
keywords, and URL shorteners.


"""

# Library imports
import requests
import tldextract

# Local imports
import config 

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
        extracted = tldextract.extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}"
        return domain.lower() in config.URL_SHORTENERS
    except Exception:
        return False
    
def check_if_https(url: str) -> bool:
    """
     check if URL uses HTTPS else raise flag
    """

    if not url.lower().startswith("https://"):
        return True