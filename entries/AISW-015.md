# AISW-015: Logging-Induced Sensitive Data Exposure

| Field | Value |
|-------|-------|
| **Identifier** | AISW-015 |
| **Rank** | #15 of 25 |
| **Severity** | HIGH |

---

## Description

AI-generated observability code — logging, tracing, error reporting, and telemetry — dumps sensitive data into log streams: full request/response payloads containing tokens, session cookies, PII, credentials, and internal object state.

Models generate verbose logging because training data overwhelmingly demonstrates logging for debugging, not production security. The result is a persistent, growing exposure surface accessible to a broad set of internal users with log access.

## Exploit Scenario

A developer asks an AI assistant to add logging to an authentication service. The generated code logs the full request body at INFO level for every authentication attempt, including the plaintext password field. Logs are shipped to a centralized logging platform accessible to the entire engineering team.

A disgruntled contractor with log access harvests passwords from authentication logs and uses credential stuffing against other services where users have reused passwords.

## Detection Methods

- Log scanning tools that detect PII, credentials, tokens, and high-entropy strings in log output
- CI-time analysis of logging statements checking for sensitive field names in logged objects
- Runtime sampling of log output with automated PII detection and alerting
- Log access auditing correlating who reads logs with what sensitive data they contain

## Mitigations

- Implement structured logging with explicit allow-lists of loggable fields; never log full request/response objects
- Provide a logging wrapper library that automatically redacts known sensitive field patterns
- Classify log levels by audience: DEBUG (dev only, never production), INFO (operational, no PII), ERROR (diagnostic, redacted)
- Require security review for any logging changes in authentication, payment, or PII-handling services

## Related Mappings

- **CWE-532**: Insertion of Sensitive Information into Log File
- **CWE-209**: Generation of Error Message Containing Sensitive Information
- **OWASP LLM06**: Sensitive Information Disclosure

## Severity Rationale

Ranked HIGH because logging is generated for every service and rarely reviewed with the same scrutiny as business logic. Sensitive data in logs creates a persistent, growing exposure surface accessible to a broad set of internal users.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
