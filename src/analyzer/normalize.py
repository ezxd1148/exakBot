# libraries

from urllib.parse import urlparse, urlunparse
import idna

def normalize_link(url: str) -> str:
    """
    This function will normalizes URL from bot.py
    """
    # remove whitespaces & lowercase whole link
    url = url.strip()

    # strip wrapper punctuation 
    wrapper_chars = '()[]{}<>"\''
    while url and url[0] in wrapper_chars and url[-1] in wrapper_chars:
        url = url[1:-1].strip()

    # strip trailing independently
    # this must include things like = . , ; ! ? :

    trailing_chars = '.,;!?:'
    while url and url[-1] in trailing_chars:
        url = url[:-1].strip()
    # only allow if link has http or https
    # else ignore the link
    # ignore: IP, ftp, mailto, file:, data:, javascript:, vbscript:, etc. -- IMPORTANT
    # this is to avoid false positives and security risks and also follow the SECURITY.md guidelines
    if not (url.lower().startswith("http://") or url.lower().startswith("https://")):
        # join http:// or https:// if missing
        # but reject link if startswith other scheme
        return "False link, missing or invalid scheme (we strictly suggest including http/https only)"
    
    # URL parser to split scheme, hostname, port, parh, query, fragment
    # also reject if hostname is missing
    parsed = urlparse(url)
    if not parsed.hostname:
        return "False link, hostname missing"
    
    scheme = parsed.scheme.lower()
    host = parsed.hostname.lower().rstrip('.') # add optional IDNA conversion (idna library)
    idnahost = idna.encode(host).decode('utf-8')
    # detect if conversion happens
    if idnahost != host:
        # raise flag for punycode usage, in the future add risk scoring rule
        host = idnahost

    port = parsed.port

    # detect if username or password is present in URL
    if parsed.username or parsed.password:
        # keep normalizing but warn user, in the future add risk scoring rule
        pass

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