# ExakBot (MVP) – Telegram Link Triage Bot

ExakBot is a lightweight Telegram bot that helps users **triage suspicious links** (phishing/scam/malware delivery style) by running **fast, explainable checks** and returning a **risk level + reasons + safe next steps**.

It’s designed to be:
- **Easy**: paste a link, get a result
- **Explainable**: every score comes with reasons
- **Safe**: hardened against obvious abuse (SSRF-style misuse)
- **Deployable**: runs as a small service (Docker-friendly)

> Disclaimer: This is a **triage tool**, not an oracle. It helps you decide whether a link looks risky. It does not guarantee that a link is safe or malicious.

---

## What it does

When a user sends a URL (or forwards a message containing URLs), ExakBot will:

1. **Extract** URLs from the message
2. **Normalize** them (clean formatting, ensure valid scheme)
3. **Resolve redirects safely** (with strict timeouts and limits)
4. **Analyze signals** (domain + URL patterns + redirect behavior)
5. Return:
   - **Risk level** (Low / Medium / High)
   - **Score** (0–100)
   - **Final destination domain**
   - **Redirect chain summary**
   - **Top reasons** (explainable triggers)
   - **Recommended next steps**

---

## What it does NOT do (by design)

ExakBot deliberately avoids high-risk or heavy features in the MVP:

- ❌ No file detonation / sandboxing
- ❌ No attachment execution or macro detonation
- ❌ No crawling full websites or downloading large content
- ❌ No “guaranteed malicious” claims
- ❌ No internal network scanning (private IPs are blocked)

If you need deep malware analysis, use dedicated tools and controlled environments.

---

## Example output

**Input**

Example.com

**Output (example)**
- **Risk:** High (78/100)
- **Final:** `example-login[.]com`
- **Redirects:** `bit.ly → t.co → example-login.com`
- **Why:**
  - URL shortener used (+20)
  - Redirect chain length: 2 (+10)
  - Punycode / homograph risk (+20)
  - Final URL is not HTTPS (+30)
- **Next steps:**
  - Don’t enter credentials
  - Verify via official app/site
  - If you already interacted: change password + enable 2FA

---

## Detection philosophy (explainable scoring)

ExakBot uses a simple points-based system:

- **Score:** 0–100
- **Risk Levels:**
  - **Low**: 0–24
  - **Medium**: 25–59
  - **High**: 60–100

Each score is built from triggered rules. Example signals include:

### URL + domain signals
- URL shorteners (e.g., bit.ly, t.co)
- IP-literal URLs (e.g., `http://185.10.10.10/...`)
- Punycode / `xn--` domains (possible homograph)
- Suspicious URL structure (very long URLs, heavy encoding, `@` in URL)
- Excessive subdomains
- Suspicious TLDs (small curated list)

### Redirect behavior
- Multiple redirects
- Final destination differs significantly from the original domain

### Transport
- Final URL missing HTTPS (strong risk indicator)

> Important: A legit link can trigger some signals, and a malicious link can sometimes look “clean.” The point is **triage and caution**, not certainty.

---

## Safety & abuse resistance

Because this bot is public-facing, it includes safeguards to reduce misuse:

### SSRF prevention (hard block)
ExakBot refuses to fetch or resolve targets that:
- point to **private/internal IP ranges** (e.g., `127.0.0.1`, `192.168.x.x`, `10.x.x.x`, etc.)
- resolve via DNS to local/private ranges
- use disallowed schemes (non-HTTP/S)
- include localhost or internal hostnames

### Limits
- Max redirects (default: 5)
- Strict timeouts for network calls
- Limits on number of URLs analyzed per message
- Optional caching (same link hash → fast result)
- Optional per-user rate limiting (prevents spam and server abuse)

---

## Privacy

This project aims to minimize data collection.

**Default intent:**
- No long-term storage of full user messages.
- Avoid storing full URLs. If logging is enabled, store only:
  - hashed URL (SHA256 of normalized URL)
  - timestamp
  - score + triggered rules
  - coarse metrics (latency, cache hit)

See `PRIVACY.md` for details.

---

## Usage (Telegram)

- Start the bot and paste a link
- Or forward a suspicious message containing a link
- For multiple links, the bot analyzes the first **N** (configurable)

### Recommended usage tips for users
- Prefer sending the **exact link** you received
- If the message contains multiple links, send the one you’re most unsure about
- If a link is marked Medium/High, verify through official channels instead of clicking

---

## Configuration

ExakBot is configured primarily via environment variables (see `.env.example`).

Typical parameters:
- Telegram bot token
- Redirect/timeouts limits
- URL-per-message limit
- Cache TTL
- Rate limit parameters
- Logging level

---

## Roadmap

Planned upgrades after MVP stability:

- Reputation enrichment (carefully rate-limited + cached)
- Improved lookalike detection (curated brand list + similarity)
- Optional bilingual output templates (EN/BM)
- Group-chat mode improvements (mention-only responses)
- Better analytics and monitoring

---

## Responsible use

This tool is meant for **defensive triage** and user safety.

- Do not use it to scan internal networks.
- Do not use it as a proxy to hammer websites.
- Do not rely on it as the only security decision-maker.

If you suspect an active phishing campaign, report it through appropriate channels.

---

## Contributing

Contributions are welcome, especially:
- More test cases for tricky URLs
- Scoring rule improvements (with clear reasoning)
- Better output formatting and UX
- Bug fixes for URL parsing and redirect handling

Please:
- Open an issue first for major changes
- Keep rules explainable and test-backed

---

## Security

If you find a vulnerability (especially SSRF-related):
- Please report it responsibly.
- See `SECURITY.md` for disclosure guidance.

---

## License

This project is licensed under the terms in the `LICENSE` file.

---

## Credits

Built as a practical cybersecurity project focused on:
- explainable triage,
- safe network behavior,
- and real-world usability for everyday users.

