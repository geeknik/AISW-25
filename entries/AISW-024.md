# AISW-024: Policy-to-Code Drift

| Field | Value |
|-------|-------|
| **Identifier** | AISW-024 |
| **Rank** | #24 of 25 |
| **Severity** | MEDIUM |

---

## Description

Security policies, compliance requirements, and access control specifications define one set of rules, while AI-generated enforcement logic implements a looser, more permissive version. The drift occurs because the model translates policy intent into code approximations that satisfy functional testing but miss edge cases, exception handling, and boundary conditions specified in the policy.

AI-generated code accelerates drift because models have no awareness of organizational policy context. The compliance and regulatory consequences can be severe.

## Exploit Scenario

A data retention policy specifies that customer data must be purged within 30 days of account deletion, with purge verified by audit log entry. An AI assistant generates the deletion logic with a 30-day delayed job, but the job only soft-deletes records (sets a `deleted_at` flag) rather than performing hard deletion. Backups containing the data are not addressed. No audit log entry is generated for the purge.

A compliance audit 18 months later reveals that "deleted" customer data is still recoverable from both the primary database and backups, violating GDPR right-to-erasure requirements.

## Detection Methods

- Automated compliance testing that verifies policy requirements against actual code behavior end-to-end
- Policy-code mapping documentation requiring explicit traceability from each policy clause to its implementation
- Periodic audit comparing declared policies against observed system behavior (not just code review)
- Data lineage tracking that verifies deletion, retention, and access control policies are enforced at every storage layer

## Mitigations

- Generate compliance test cases directly from policy documents and run them as mandatory CI gates
- Require traceability matrices linking each policy clause to specific code, tests, and runtime verification
- Implement policy-as-code frameworks that enforce retention, access, and deletion rules at the infrastructure layer
- Conduct regular adversarial compliance testing that attempts to recover "deleted" data and access "restricted" resources

## Related Mappings

- **CWE-284**: Improper Access Control
- **CWE-404**: Improper Resource Shutdown or Release

## Severity Rationale

Ranked MEDIUM because policy drift is slow-moving and typically discovered through audit rather than attack. However, the compliance and regulatory consequences can be severe, and AI-generated code accelerates drift because models have no awareness of organizational policy context.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
