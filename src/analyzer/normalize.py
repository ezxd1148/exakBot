# libraries

from urllib.parse import urlparse, urlunparse
from urlextract import URLExtract
import ipaddress

# maybe in the future use tldextract for better TLD handling
import idna

def normalize_link(url: str) -> str:
    """
    This function will normalizes URL from bot.py

    goal 5/2 : use urlextract to extract URL from text input (done)
    """

    extract = URLExtract() # initialize extractor

    urls_found = extract.find_urls(url) # this will extract urls from text input
    if not urls_found:
        raise ValueError("No valid URL found in the input text.")

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

    # detect if URL is IP address
    parsed_ip = urlparse(url)
    hostname_ip = parsed_ip.hostname
    if hostname_ip:
        try:
            ipaddress.ip_address(hostname_ip)
            raise ValueError("Enter a valid URL, IP address detected.")
        except ValueError:
            pass 

    # this is to avoid false positives and security risks and also follow the SECURITY.md guidelines
    if not (url.lower().startswith("http://") or url.lower().startswith("https://")):
        # UPDATE: strictly require scheme
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")
    
    # URL parser to split scheme, hostname, port, parh, query, fragment
    # also reject if hostname is missing
    parsed = urlparse(url)
    if not parsed.hostname:
        return "False link, hostname missing"
    
    scheme = parsed.scheme.lower()
    host = parsed.hostname.lower().rstrip('.')
    try: 
        idnahost = idna.encode(host).decode('utf-8')
        # detect if conversion happens
        if idnahost != host:
        # raise flag for punycode usage, in the future add risk scoring rule
            host = idnahost

    except idna.IDNAError:
        return "False link, invalid hostname encoding"
    
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