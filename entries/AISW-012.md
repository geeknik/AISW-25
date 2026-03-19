# AISW-012: Patch Placebo

| Field | Value |
|-------|-------|
| **Identifier** | AISW-012 |
| **Rank** | #12 of 25 |
| **Severity** | HIGH |

---

## Description

When asked to fix a reported vulnerability, AI generates a change that addresses the symptom, renames variables, adds superficial validation, or relocates the vulnerable code — but leaves the underlying exploit path intact. The fix satisfies the ticket, passes CI, and closes the issue while the vulnerability remains exploitable.

Placebo fixes are uniquely dangerous because they consume the organization's remediation effort, close tracking tickets, and restore false confidence while the vulnerability remains live.

## Exploit Scenario

A security scanner reports a SQL injection in a search endpoint. A developer asks an AI assistant to fix it. The assistant adds input length validation and wraps the query in a try/except block, but continues to use string formatting for query construction instead of parameterized queries.

The scanner's specific test payload is now blocked by the length check, so the scanner reports the issue as fixed. An attacker uses a shorter injection payload that bypasses the length validation and exploits the still-vulnerable string-formatted query.

## Detection Methods

- Verification testing that uses multiple attack vectors beyond the original report to confirm root-cause remediation
- Mandatory root-cause analysis documentation for every security fix, reviewed by security team
- Re-scanning with expanded payloads after every security patch, not just the original detection signature
- Code review specifically examining whether fixes address root cause vs. symptom

## Mitigations

- Require security fixes to include root-cause documentation: what the vulnerability class is, why the fix addresses it at the correct layer
- Mandate that security patches are reviewed by someone who understands the vulnerability class, not just the codebase
- Implement regression test suites for each vulnerability class that test the underlying weakness, not just the reported payload
- Prohibit AI-generated security fixes from being merged without security team approval

## Related Mappings

- **CWE-89**: SQL Injection (in example)
- **CWE-116**: Improper Encoding or Escaping of Output

## Severity Rationale

Ranked HIGH because placebo fixes are uniquely dangerous: they consume the organization's remediation effort, close tracking tickets, and restore false confidence while the vulnerability remains. The feedback loop between reporting and remediation is corrupted.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
