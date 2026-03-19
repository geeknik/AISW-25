# AISW-022: Auto-Remediation Regression

| Field | Value |
|-------|-------|
| **Identifier** | AISW-022 |
| **Rank** | #22 of 25 |
| **Severity** | MEDIUM |

---

## Description

Automated AI-powered remediation bots that fix vulnerabilities or dependency issues inadvertently re-open previously closed vulnerability classes. The bot's local context does not include the security reasoning behind the original implementation decisions, causing it to "fix" one problem while undoing a prior security fix.

As auto-remediation adoption increases, this weakness will likely rise in severity because the bot's authority to modify security-critical code is growing faster than its contextual understanding.

## Exploit Scenario

An auto-remediation bot upgrades a logging library to fix a known CVE. The new version of the library changes the default serialization format. A previous security fix had specifically configured the old version to use safe serialization.

The bot's upgrade removes the custom configuration because it's no longer compatible with the new version's API, reverting to the new version's default — which happens to use unsafe deserialization. The original vulnerability (unsafe deserialization) is re-introduced through a "security" update.

## Detection Methods

- Regression test suites specifically for previously fixed vulnerabilities, run after every automated remediation
- Change tracking that flags removal or modification of code tagged with security-fix annotations
- Automated comparison of security configurations before and after bot-generated changes
- Security fix documentation (inline comments, commit messages) that bots can parse to understand constraints

## Mitigations

- Tag all security fixes with machine-readable annotations that auto-remediation bots must preserve
- Require that auto-remediation PRs pass the full security regression test suite, not just functional tests
- Implement a security configuration lockfile that prevents automated tools from modifying security-critical settings
- Require human security review for any automated change that touches previously fixed vulnerability areas

## Related Mappings

- **CWE-693**: Protection Mechanism Failure

## Severity Rationale

Ranked MEDIUM because auto-remediation is still an emerging practice, limiting the current attack surface. As adoption increases, this weakness will likely rise in severity because the bot's authority to modify security-critical code is growing faster than its contextual understanding.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
