"""
this is the config file for everything

IMPORTANT: 
    - do not put sensitive data here, use environment variables instead
    - PLEASE check for typos and syntax errors when editing this file
"""

# Environment Variables
import os
from dotenv import load_dotenv

# load env
load_dotenv()

# get telegram bot token from env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

## check if token is missing
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in Environment Variable")

# resolver.py
# this is used for risk scoring and flag detection

## timeout for requests in seconds
REQUEST_TIMEOUT = 5

## high risk TLDs used for phshing
SUSPICIOUS_TLDS = {
    'xyz', 'top', 'gq', 'cn', 'zip', 'mov', 'link', 'click', 
    'rest', 'fit', 'tk', 'ml', 'ga', 'cf', 'work', 'loan', 
    'kim', 'country', 'science', 'party'
}

## common suspicious words in URL
SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'update', 'secure', 'account', 
    'banking', 'password', 'signin', 'confirm', 'ebayisapi',
    'webscr', 'paypal', 'cmd', 'service', 'support', 
    'billing', 'wp-admin', 'admin', 'user', 'client', 'auth', 'unlock', '@'
]

## common URL shortener domains
URL_SHORTENERS = [
    'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co', 
    'buff.ly', 'adf.ly', 'bit.do', 'cutt.ly', 'is.gd', 
    'soo.gd', 's2r.co', 'clicky.me', 'shorturl.at'
]

## user agent for requests
USER_AGENT = "ExakBot/1.0 (Security Triage Bot) + github.com/ezxd1148/exakBot"