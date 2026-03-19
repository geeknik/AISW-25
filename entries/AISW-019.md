# AISW-019: Vulnerable Migration and Rollback Scripts

| Field | Value |
|-------|-------|
| **Identifier** | AISW-019 |
| **Rank** | #19 of 25 |
| **Severity** | MEDIUM |

---

## Description

AI-generated database migration, schema change, and rollback scripts bypass validation constraints, expose data during transformation, create unsafe intermediate states, or fail to handle partial completion.

These scripts often run with elevated database privileges and are tested less rigorously than application code. AI-generated migrations are particularly dangerous because the model optimizes for completion rather than transactional safety.

## Exploit Scenario

A developer asks an AI assistant to generate a migration that encrypts a plaintext PII column in a production database. The generated script creates a new encrypted column, copies data from the plaintext column to the encrypted column, then drops the plaintext column.

However, the migration has no transaction wrapping. If it fails after copying but before dropping, both plaintext and encrypted columns exist simultaneously. The generated rollback script decrypts the data back to plaintext — creating a window where encryption can be trivially reversed. Additionally, the migration logs each row being processed, including the plaintext values, to the migration output.

## Detection Methods

- Migration review requiring transaction safety analysis and rollback state audit for every schema change
- Automated testing of migration scripts in staging with simulated failures at each step
- Log scanning of migration output for sensitive data exposure
- Database privilege auditing confirming migrations run with minimum necessary permissions

## Mitigations

- Require all migrations to be transactional with explicit rollback handling for every intermediate state
- Mandate that migration scripts are reviewed by DBA or security team, not just application developers
- Test migrations with injected failures (killed process, disk full, network partition) to verify safe intermediate states
- Never log data content during migration operations; log only row counts and status

## Related Mappings

- **CWE-311**: Missing Encryption of Sensitive Data
- **CWE-532**: Insertion of Sensitive Information into Log File

## Severity Rationale

Ranked MEDIUM because migration scripts run infrequently but with high privilege and low review scrutiny. AI-generated migrations are particularly dangerous because the model optimizes for completion rather than transactional safety.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
