# libraries

from urllib.parse import urlparse, urlunparse

def normalize_link(url: str) -> str:
    """
    This function will normalizes link from bot.py
    """
    # remove whitespaces & lowercase whole link
    url = url.strip()

    # strip wrapper punctuation 
    wrapper_chars = '()[]{}<>"\''
    while url and url[0] in wrapper_chars and url[-1] in wrapper_chars:
        url = url[1:-1].strip()

    # strip trailing wrapper independently
    # this must include things like = . , ; ! ? :

    trailing_chars = '.,;!?:'
    while url and url[-1] in trailing_chars:
        url = url[:-1].strip()

    # only allow if link has http or https
    # else ignore the link
    # ignore: IP, ftp, mailto, file:, data:, javascript:, vbscript:, etc. -- IMPORTANT
    # this is to avoid false positives and security risks and also follow the SECURITY.md guidelines
    if not (url.startswith("http://") or url.startswith("https://")):
        return "False link, only http/https allowed"
    
    # URL parser to split scheme, hostname, port, parh, query, fragment
    # also reject if hostname is missing
    parsed = urlparse(url)
    if not parsed.hostname:
        return "False link, hostname missing"
    
    scheme = parsed.scheme.lower()
    host = parsed.hostname.lower().rstrip('.')
    port = parsed.port

    use_port = port is not None and not (
        (scheme == "http" and port == 80) or 
        (scheme == "https" and port == 443)
    )

    netloc = f"{host}:{port}" if use_port else host

    normalized = urlunparse((
        scheme,
        netloc,
        parsed.path or '/',
        '',  # params
        parsed.query,
        ''   # fragment
    ))

    return normalized