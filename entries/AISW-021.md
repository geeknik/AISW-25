# AISW-021: Review Evasion by Diff Inflation

| Field | Value |
|-------|-------|
| **Identifier** | AISW-021 |
| **Rank** | #21 of 25 |
| **Severity** | MEDIUM |

---

## Description

AI-generated code changes produce large, plausible-looking diffs that dilute reviewer attention. The exploitable pattern — whether intentionally injected or accidentally generated — is buried in hundreds of lines of correct, well-structured code.

Reviewers experience cognitive overload and approve the entire change without interrogating every line. AI generation dramatically increases the volume and plausibility of large diffs, amplifying this risk beyond what manual coding produces.

## Exploit Scenario

A developer asks an AI assistant to refactor a 500-line module. The assistant produces a 400-line diff that restructures the code, improves naming, and adds documentation. Buried in the refactor is a subtle change: a permission check that previously required `admin AND owner` now requires `admin OR owner`.

The change is syntactically minimal (one character) but semantically critical. Three reviewers approve the PR based on the overall quality of the refactor. The privilege escalation ships to production.

## Detection Methods

- Diff analysis tools that flag semantic changes in permission logic, authentication code, and security-critical conditions
- Mandatory splitting of large PRs into functional units, each reviewed independently
- Automated security-focused diff scanning that highlights changes to authorization predicates, regardless of PR size
- Review metrics tracking approval speed vs. diff size to detect rubber-stamping patterns

## Mitigations

- Enforce maximum PR size limits, with mandatory splitting for changes above threshold
- Require separate PRs for refactoring and behavioral changes; never combine cosmetic and functional changes
- Use automated tools that specifically highlight security-relevant diff lines for reviewer attention
- Implement mandatory security review for any PR touching authentication, authorization, or access control code, regardless of size

## Related Mappings

- **CWE-284**: Improper Access Control (as consequence)

## Severity Rationale

Ranked MEDIUM because the weakness is in the human review process rather than the code itself, but AI generation dramatically increases the volume and plausibility of large diffs, amplifying the risk.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
