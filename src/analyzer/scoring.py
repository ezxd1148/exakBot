"""
Handles scoring of URLs based on various criteria.

always remember to update

risk score should be 0 to 100

:returns: risk score as integer and list of messages
"""

# imports analyzer modules

import analyzer.resolver as resolver
from urllib.parse import urlparse

#main scoring function

def score_url(url: str) -> int:
    """
    Scores the given URL based on various risk factors.
    Returns an integer score; higher means more risky.
    """

    # for debug
    print(f"Scanning: {url}")

    final_message = []
    score = 0
    risk_level = None

    # Check for suspicious TLDs
    extracted = urlparse(url)
    hostname = extracted.hostname or ""
    tld = hostname.split('.')[-1] if '.' in hostname else ''
    if resolver.is_suspicious_tld(tld):
        final_message.append(f"Suspicious TLD detected: {tld}")
        score += 25 # high risk for suspicious TLDs

    # Check for suspicious keywords
    if resolver.contains_suspicious_keyword(url):
        final_message.append("Suspicious keyword found in URL") 
        score += 40  # moderate risk for suspicious keywords

    # Check if URL is shortened
    if resolver.is_url_shortened(url):
        final_message.append("URL is from a known URL shortener service")
        score += 20  # low risk for shortened URLs

    # check if redirects are present
    resolution = resolver.get_final_url(url)
    if resolution['error']:
        print(f"Scan failed: {resolution['error']}")
        final_message.append(f"Error during URL resolution: {resolution['error']}")
    else:
        print(f"Original: {resolution['original_url']}")
        print(f"Landed on: {resolution['final_url']}") 
        print(f"Redirects: {resolution['chain']}") # List of URLs hopped through
        score += len(resolution['chain']) * 5 # adds up risk for each hops
        final_message.append(f"Final URL after redirects: {resolution['final_url']}, Number of hops: {len(resolution['chain'])}")

    # check if https
    if not extracted.scheme.lower() == "https":
        final_message.append("URL does not use HTTPS")
        score += 30
         # moderate risk for non-HTTPS URLs

    # check if punycode is present
    if 'xn--' in hostname:
        final_message.append("Punycode detected in hostname")
        score += 20
    
    # cap score at 100
    if score > 100:
        score = 100

    # check risk level
    if score >= 60:
        risk_level = "High Risk"
    elif score >= 25 and score < 60:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return score, final_message, risk_level