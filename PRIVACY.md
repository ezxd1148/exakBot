# Privacy Policy (PRIVACY.md)

This project is a Telegram bot that analyzes links users send to it. That means it touches user-provided content, which means we have to be clear about what is and isn’t collected.

This document explains:
- what data the bot processes,
- what it stores (if anything),
- what it logs,
- and what users can expect.

**Short version:** the bot tries to collect as little as possible, because storing people’s stuff is how you accidentally become a liability.

---

## 1) What data the bot processes

When you send a message to the bot, it may process:

### A) Message content (transient)
- The text you send, including any URLs in it
- If you forward a message, the forwarded text is processed to extract URLs

This content is processed **in memory** to extract and analyze URLs.

### B) URL network metadata (transient)
To analyze a URL, the bot may fetch lightweight metadata:
- redirect chain (e.g., `bit.ly → ... → final-domain`)
- HTTP status codes
- final destination URL
- response headers (limited set, if needed)
- content type (if available)

The bot is designed to avoid downloading full page content unless explicitly required for safe redirect resolution, and even then it should enforce strict timeouts and size limits.

---

## 2) What data the bot stores

### Default intent: no long-term storage of personal content
The bot is built to function without storing:
- full Telegram messages
- user chat history
- full URLs
- personal identifiers beyond what Telegram sends for routing

However, some minimal data may be stored depending on configuration.

### Optional: minimal operational logging (recommended for debugging)
If logging is enabled, the project should store **minimal, non-sensitive** records such as:
- timestamp
- risk score and triggered rules
- latency (processing time)
- error type (timeout, invalid URL, blocked target)
- *optionally*: hashed URL for deduplication and caching

**Hashed URL (recommended):**
- Store `SHA256(normalized_url)` instead of the raw URL.
- This supports caching and debugging without storing the original.

> Note: Hashing does not make something magically anonymous in all cases, but it is significantly safer than storing raw URLs.

### What the bot should NOT store (unless you deliberately change it)
- full raw URLs for long periods
- full messages or forwarded message text
- IP addresses of users (Telegram already has infrastructure-level metadata; this bot should not add extra tracking)
- any credentials, tokens, or personally sensitive data

---

## 3) What the bot logs

Logs are intended for:
- debugging crashes
- measuring reliability and performance
- preventing abuse

By default, logs should be configured to avoid recording:
- full message content
- raw URLs
- personal details

### Good logging examples
- `"blocked_private_ip": true`
- `"risk_level": "High"`
- `"score": 78`
- `"rules": ["shortener_used", "no_https_final"]`
- `"latency_ms": 2431`

### Bad logging examples
- raw message bodies
- full URLs and query strings
- pasted credentials (yes, users do this)
- anything that could identify a user beyond Telegram’s necessary routing data

---

## 4) Data retention

Retention depends on how you deploy the bot.

Recommended defaults:
- **No persistent storage** for message contents
- Logs (if enabled): keep for **7–30 days**, then delete/rotate
- Cache (if enabled): keep for **6–24 hours** per URL hash

If you deploy on a platform that automatically stores logs, check that platform’s retention settings.

---

## 5) Who can access data

- Bot operators (maintainers) can access whatever is stored on the bot host (logs, cache, metrics).
- Telegram itself processes messages according to Telegram’s own privacy policy and infrastructure behavior.

This bot cannot control Telegram’s policies, but it can avoid adding extra data collection on top.

---

## 6) Security measures related to privacy

To reduce privacy and abuse risks, the bot includes safeguards such as:
- SSRF prevention: blocks private/local IP ranges and internal hosts
- strict timeouts and redirect limits
- rate limiting (to prevent spam / scraping)
- optional caching using hashed URLs

If you find a privacy-impacting bug (e.g., data exposure through logs), report it via `SECURITY.md`.

---

## 7) User responsibilities

Please do not send:
- passwords
- OTP codes
- private documents
- personal identity information

The bot is meant to analyze links, not store sensitive personal data.

---

## 8) Changes to this policy

This policy may be updated as the project evolves (especially if new features like file scanning or third-party reputation checks are added).

If major data handling changes occur, this document should be updated to reflect them.

---

## Contact

For privacy or security concerns, follow the reporting instructions in:
- `SECURITY.md`

---

**Summary (again):** the bot processes your message to extract and analyze links, and it aims to store as little as possible. Because the best way to protect data is to not collect it in the first place.
