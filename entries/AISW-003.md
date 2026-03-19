# AISW-003: Dependency Confabulation and Typosquat Intake

| Field | Value |
|-------|-------|
| **Identifier** | AISW-003 |
| **Rank** | #3 of 25 |
| **Severity** | CRITICAL |

---

## Description

AI models suggest package names that do not exist or are subtly misspelled versions of real packages. When developers install these hallucinated dependencies, attackers who have registered the confabulated package names on public registries achieve code execution in the target environment.

The attack is amplified because models consistently hallucinate the same nonexistent package names, making typosquat registration predictable and scalable. Research has demonstrated that monitoring LLM-suggested package names and pre-registering them is a viable, low-cost attack strategy.

## Exploit Scenario

A developer asks a coding assistant to generate a Python script for PDF watermarking. The assistant suggests `pip install pdf-watermarker`, a package that does not exist on PyPI. An attacker who has been monitoring LLM-suggested package names has already registered `pdf-watermarker` with a payload that exfiltrates environment variables on import.

The developer installs the package, the payload executes during import, and AWS credentials from the developer's environment are sent to the attacker's collection endpoint. The same hallucinated name is suggested to hundreds of developers asking similar questions.

## Detection Methods

- Pre-install validation that checks package existence, age, maintainer reputation, and download count against thresholds
- Monitoring LLM outputs for package suggestions and cross-referencing against known-good package registries
- Registry-side detection of newly registered packages whose names match common LLM hallucination patterns
- Network monitoring for unexpected outbound connections during package installation

## Mitigations

- Enforce allow-listed package registries with curated, pre-approved package sets for all AI-suggested dependencies
- Require lockfile-based installs only; never run bare `pip install` or `npm install` from AI suggestions without verification
- Implement organizational package proxies that block installation of packages below minimum age/download thresholds
- Run all AI-suggested package installations in isolated environments with no access to credentials or production networks

## Related Mappings

- **CWE-829**: Inclusion of Functionality from Untrusted Control Sphere
- **CWE-1357**: Reliance on Insufficiently Trustworthy Component
- **OWASP LLM05**: Supply Chain Vulnerabilities

## Severity Rationale

Ranked #3 because the attack is trivially scalable: one package registration can compromise thousands of developers who receive the same hallucinated suggestion. The supply chain entry point bypasses all application-layer defenses. Models hallucinate deterministically for common queries, making the attack surface predictable and farmable.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
