# AISW-009: Stale Vulnerable Pattern Regeneration

| Field | Value |
|-------|-------|
| **Identifier** | AISW-009 |
| **Rank** | #9 of 25 |
| **Severity** | HIGH |

---

## Description

AI models regenerate insecure coding patterns that were deprecated or patched years ago because these patterns remain heavily represented in training data and retrieval corpora. The model has no mechanism to distinguish "common" from "currently recommended," causing known-vulnerable approaches to be continuously reintroduced into modern codebases.

This is not a model error — it is a statistical inevitability. Insecure patterns dominate training distributions because they were written for years before secure alternatives were established.

## Exploit Scenario

A developer requests XML parsing code. The assistant generates a solution using `lxml.etree.parse()` with default settings that enable external entity processing, a vulnerability class (XXE) that has been well-understood since 2013. The model generates this pattern because thousands of pre-2015 code samples in its training data use the same default.

The application processes user-uploaded XML files, allowing an attacker to read arbitrary files from the server using a crafted DTD entity.

## Detection Methods

- SAST rules specifically targeting deprecated API usage and known-insecure default configurations
- Dependency analysis flagging the use of deprecated function signatures even when they compile successfully
- Organizational banned-pattern lists integrated into linting and CI scanning
- Regular auditing of AI-generated code against current CVE databases for pattern matches

## Mitigations

- Maintain and enforce an organizational banned-patterns list that overrides AI suggestions at the linter level
- Inject current security best-practice guides as retrieval context for all AI coding sessions
- Require that AI-generated code targeting parsing, serialization, or cryptographic operations is reviewed against current OWASP cheat sheets
- Periodically retrain or re-configure retrieval pipelines to deprioritize code samples older than a defined threshold

## Related Mappings

- **CWE-477**: Use of Obsolete Function
- **CWE-1104**: Use of Unmaintained Third Party Components

## Severity Rationale

Ranked HIGH because the training data distribution guarantees that insecure patterns will be the most statistically likely completions. Unlike novel bugs, these are known vulnerabilities being reintroduced at scale. Existing detection tooling can catch many instances, which prevents CRITICAL ranking.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
