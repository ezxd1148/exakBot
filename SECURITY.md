# Security Policy (SECURITY.md)

Thanks for helping make this project less fragile. Security reports are welcome, especially for anything that could let the bot be abused (SSRF, request smuggling, bypassing blocks, token leaks, etc.).

This file explains:
- what counts as a security issue,
- what **not** to do,
- how to report responsibly,
- and what to expect.

---

## Supported Versions

This project is currently in MVP development.

Security fixes are provided for:
- **The latest `main` branch**, and
- **The latest tagged release** (if releases exist)

Older tags/releases may not receive patches.

---

## What to Report (High Priority)

Please report any vulnerability that could cause one or more of the following:

### 1) SSRF / Internal Network Access
Anything that allows fetching, resolving, or reaching:
- private IP ranges (e.g., `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)
- localhost (`127.0.0.0/8`, `::1`, `localhost`)
- link-local / ULA IPv6 ranges (`fe80::/10`, `fc00::/7`)
- internal hostnames or `.local` domains
- cloud metadata endpoints (example: `169.254.169.254`)

### 2) Rate-limit Bypass / Abuse Amplification
- bypassing per-user throttling
- causing the bot to fetch many URLs per message
- causing expensive work repeatedly (cache busting)
- any path that turns the bot into a free scanning proxy

### 3) Remote Code Execution / Command Injection
- any user-controlled input reaching shell commands
- unsafe deserialization
- template injection
- dynamic imports / eval usage mistakes

### 4) Sensitive Data Exposure
- leaking bot token
- leaking user data that should not be logged
- exposing full URLs/messages when logging is claimed to be minimal
- accidentally publishing private emails/credentials in logs

### 5) Dependency / Supply Chain Risks
- vulnerable dependencies that materially affect the bot
- insecure default configs
- unsafe build pipeline behavior

---

## What is NOT a Security Issue

Some things are expected limitations of a triage tool:

- The bot marks a link “Low risk” but it is actually malicious.
- The scoring rules don’t match your personal opinion.
- A malicious link uses a clean domain and bypasses heuristic checks.
- “It should integrate VirusTotal / Safe Browsing” (feature request, not security).

If you have improvements, open an issue as a feature suggestion.

---

## Reporting a Vulnerability

### Preferred method
Open a **GitHub Security Advisory** (private report) if this repository has Security Advisories enabled.

### If Security Advisories are not enabled
Create a GitHub issue with:
- minimal details that don’t enable abuse
- a note requesting private follow-up

Then the maintainer will respond and move details to a safer channel.

> Please do **not** publish a working exploit in a public issue.

---

## What to Include in Your Report

To help reproduce and fix fast, include:

1. **Summary** of the issue
2. **Impact** (what an attacker can do)
3. **Steps to reproduce**
4. **Proof-of-concept (PoC)**:
   - keep it minimal
   - avoid real-world targets
   - prefer local test URLs or benign endpoints
5. **Expected vs actual behavior**
6. Any relevant logs (remove sensitive data)

If the issue is SSRF-related, include:
- the exact URL(s) used
- redirect chain (if any)
- whether DNS rebinding is involved
- whether IPv6 is involved

---

## Responsible Disclosure Guidelines

Please follow these rules:

- Don’t exploit against targets you don’t own or have permission to test.
- Don’t attempt to access internal systems or cloud metadata.
- Don’t spam the live public bot to test rate limiting.
- If you discover a critical issue, **do not share it publicly** until a fix is released.

---

## Response Targets

Because this is an MVP project (not a corporation), response times vary. Typical goals:

- Acknowledge report: within **7 days**
- Triage + confirm: within **14 days**
- Patch for confirmed critical issues: as soon as practical

---

## Security Design Notes (For Reviewers)

This bot includes protections intended to reduce abuse:

- Scheme allowlist: HTTP/S only
- Redirect limits + strict timeouts
- DNS resolution checks
- Private IP range blocking (IPv4 + IPv6)
- Localhost/internal hostname blocking
- Optional caching + rate limiting
- Minimal logging intent (avoid storing full URLs/messages)

If you find a bypass, that’s exactly what we want to hear about.

---

## Credit

If you want credit:
- Include the name/handle you want credited with in the report.
- If you prefer anonymity, say so.

---

Thank you for making the bot safer for everyone who insists on clicking things.
