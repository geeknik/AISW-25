# AISW-005: Secret Reintroduction by Completion

| Field | Value |
|-------|-------|
| **Identifier** | AISW-005 |
| **Rank** | #5 of 25 |
| **Severity** | HIGH |

---

## Description

During code refactoring, migration, or feature addition, AI models re-introduce hardcoded secrets, test credentials, API keys, or insecure `.env` handling patterns that were previously removed. The model's completion behavior draws from training data and local context where hardcoded values are common, overriding the project's established secret management practices.

This is a regression weakness: teams that have already solved the problem find it re-introduced by AI completions. The risk is amplified during large refactoring operations where many files are touched and review attention is diluted.

## Exploit Scenario

A team has migrated all database credentials to AWS Secrets Manager. A developer asks a coding assistant to refactor the database connection module for a new ORM. The assistant generates a new module that includes a hardcoded `DATABASE_URL` with a connection string containing username and password as a "default fallback."

The developer reviews the overall structure, approves the refactor, and merges. The hardcoded credential is a valid test database password that also works against the staging environment. The commit is pushed to a public repository fork during an open-source contribution, exposing the staging database.

## Detection Methods

- Pre-commit hooks running secret scanning (truffleHog, detect-secrets, gitleaks) on all staged changes
- CI pipeline secret scanning that blocks merges containing high-entropy strings or known credential patterns
- Repository-level branch protection requiring secret scan pass as a merge prerequisite
- Periodic scanning of all repository history for any secrets introduced by AI-assisted commits

## Mitigations

- Enforce secret scanning as a blocking CI gate with zero tolerance for detected credentials
- Configure coding assistants with project-level instructions that prohibit hardcoded credential patterns
- Remove all real credentials from training context, retrieved documents, and example code available to models
- Implement runtime secret injection only, with no filesystem-based credential storage in any environment

## Related Mappings

- **CWE-798**: Use of Hard-coded Credentials
- **CWE-312**: Cleartext Storage of Sensitive Information
- **OWASP LLM02**: Sensitive Information Disclosure

## Severity Rationale

Ranked HIGH because the failure mode is regression: teams that have already solved this problem find it re-introduced by AI completions. The blast radius depends on the secret type but can range from database compromise to full cloud account takeover. Detection tooling is mature, which prevents this from ranking CRITICAL.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
