---
name: cyber-fraud-forensics
description: Standard operating procedure for documenting a detected phishing/typosquatting/brand-clone threat and producing a technical abuse report. Use when a visual brand threat is flagged (e.g. by Aegis BrandGuard), when capturing network evidence from a suspicious site, or when assembling an abuse report (Markdown/PDF) to send to registrars or hosting providers. Covers evidence collection and report structure only — legal grounds are left as placeholders to be filled with a current, verified source on demand.
---

# cyber-fraud-forensics

SOP for turning a flagged digital-fraud threat (phishing, typosquatting, brand clone) into a clean, evidence-backed abuse report. Scope is **technical**: how to capture evidence and how to structure the report. It does **not** assert fixed legal grounds — those are placeholders the operator fills with a verified, current source per jurisdiction.

## Scope guardrail

This skill never embeds specific statutes, treaty articles, or "this violates law X" claims as fixed knowledge. Legal/policy citations age badly and a wrong citation weakens a takedown request. Wherever a legal basis is needed, emit a placeholder like `[APPLICABLE_LOCAL_LEGISLATION]` or `[REGISTRAR_ABUSE_POLICY_REF]` and flag that it must be filled from a current source. State this limitation in the report itself.

## 1. Evidence collection

Goal: capture enough that a third party (registrar, host, CERT) can independently verify the site is malicious. Collect read-only; never authenticate, submit, or interact with forms on the suspect site.

### Identity & infrastructure
- **Suspect URL(s)** — full, including path and any redirect chain. Record each hop.
- **Resolved IP(s)** — `dig +short suspect-domain.com` / `nslookup`.
- **Hosting / ASN** — reverse lookup the IP; note hosting provider and ASN (whois/RDAP).
- **Registrar & WHOIS/RDAP** — registrar name, creation date (recent registration is a strong signal), and the published **abuse contact email** — this is the address the report goes to.
- **TLS certificate** — issuer, validity dates, SANs. A cert covering the spoofed brand name or a mismatched/self-signed cert is evidence.

### Network evidence (Chrome DevTools / capture)
Open DevTools on the suspect page and document, with screenshots and exported data:
- **Network tab** — outbound requests to third-party domains; flag any POST of form data to a domain other than the displayed one (credential exfiltration). Export as HAR.
- **External scripts** — scripts loaded from unrelated domains, obfuscated JS, known phishing-kit signatures.
- **Cookies / storage** — suspicious tracking or session-harvesting cookies.
- **Console** — errors revealing kit origin or backend endpoints.
- **Sources** — note any cloned assets (logos, CSS) hot-linked from the legitimate brand's domain — direct proof of impersonation.

### Visual & integrity evidence
- Full-page **screenshot** of the clone, timestamped.
- Side-by-side with the legitimate brand page.
- **Hashes** of downloaded suspicious artifacts (`sha256sum`) so the evidence is tamper-evident.
- Capture the **HTML source** (saved, hashed) — clones often embed the original brand's metadata/paths.

### Chain of custody
For every artifact record: what it is, the exact source URL, **capture timestamp (with timezone)**, the tool used, and its hash. An abuse report with reproducible, hashed, timestamped evidence is far harder to dismiss.

## 2. Abuse report structure

Bilingual-ready (EN/PT). Keep it factual and technical; let the evidence carry the argument. Below is the skeleton — fill brackets per case.

```markdown
# Abuse Report — Phishing / Brand Impersonation
**Report ID:** [REPORT_ID]   **Date (UTC):** [TIMESTAMP]
**Reporting entity:** [REPORTER_NAME / ON_BEHALF_OF_BRAND]
**Contact:** [REPORTER_ABUSE_CONTACT]

## 1. Summary
A fraudulent site impersonating [BRAND] is active at [SUSPECT_URL].
It is [phishing for credentials / cloning the brand / typosquatting]
and is hosted on infrastructure operated by [HOSTING_PROVIDER].
We request review and takedown per your abuse policy
[REGISTRAR_OR_HOST_ABUSE_POLICY_REF].

## 2. Target of impersonation
- Legitimate brand / domain: [LEGIT_DOMAIN]
- Trademark / asset misused: [LOGO / NAME / UI — describe, attach evidence]

## 3. Malicious infrastructure
| Field | Value |
|---|---|
| Suspect domain | [DOMAIN] |
| Full URL(s) | [URLS] |
| Resolved IP(s) | [IPS] |
| Hosting provider / ASN | [HOST / ASN] |
| Registrar | [REGISTRAR] |
| Domain created | [CREATION_DATE] |
| TLS issuer / SANs | [CERT_DETAILS] |
| Abuse contact notified | [ABUSE_EMAIL] |

## 4. Evidence of malicious activity
- Credential exfiltration: [describe POST target domain ≠ displayed domain]
- External/obfuscated scripts: [list domains]
- Hot-linked brand assets: [paths proving impersonation]
- Visual clone: [screenshot ref + hash]
- HAR / console exports: [artifact refs + hashes]

### Evidence manifest (chain of custody)
| Artifact | Source | Captured (UTC) | Tool | SHA-256 |
|---|---|---|---|---|
| [file] | [url] | [ts] | [tool] | [hash] |

## 5. Requested action
Review and disable / suspend [DOMAIN or HOSTING] in accordance with
[REGISTRAR_OR_HOST_ABUSE_POLICY_REF] and
[APPLICABLE_LOCAL_LEGISLATION — to be confirmed against a current source].

## 6. Limitations
Legal references in this report are placeholders to be validated against
current, authoritative sources for the relevant jurisdiction before formal
submission. Technical evidence above is reproducible via the listed hashes.
```

## 3. Routing the report
- Send to the **registrar abuse contact** (from WHOIS/RDAP) and the **hosting provider abuse contact** (from the IP/ASN) — often different parties; notify both.
- For major providers, prefer their dedicated abuse intake (e.g. provider abuse portal) over generic email when one exists; look it up at report time rather than hardcoding it.
- Consider notifying the relevant national CERT and any brand-protection/anti-phishing feeds — look up the current intake channel; do not assume a fixed address.
- Keep the original evidence bundle (hashed) archived in case escalation is needed.

## Anti-patterns
- Asserting specific laws/articles as fact inside the report — use placeholders and flag for verification.
- Interacting with the phishing site (entering data, submitting forms) — capture read-only.
- Sending evidence without timestamps/hashes — it's dismissible.
- Hardcoding provider abuse addresses or CERT contacts that may have changed — resolve them at report time.
- Sending to only one party when registrar and host differ.
