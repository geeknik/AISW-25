# AISW-010: Excessive Agent Privilege in CI/CD

| Field | Value |
|-------|-------|
| **Identifier** | AISW-010 |
| **Rank** | #10 of 25 |
| **Severity** | CRITICAL |

---

## Description

Coding agents, automated code review bots, and AI-powered CI/CD integrations are granted repository write access, secret read access, package publishing rights, or deployment permissions that far exceed their operational requirements. When compromised through prompt injection or model misbehavior, these privileges become the attacker's privileges.

Most organizations have not yet audited non-human identity permissions in their CI/CD infrastructure. The combination of over-privileged agents and prompt injection (AISW-002) creates a reliable, repeatable attack chain against the software supply chain.

## Exploit Scenario

An organization deploys an AI code review agent with repository write access to post review comments and auto-fix trivial issues. The agent also has read access to CI secrets for running tests. An attacker submits a PR with a crafted description that instructs the agent to create a new file containing a reverse shell, commit it to a feature branch, and trigger a CI run.

The agent's write permissions allow all three actions. The CI run executes the reverse shell with access to deployment credentials stored as pipeline secrets.

## Detection Methods

- Permission auditing of all AI agents and bots, mapping granted vs. required privileges
- Behavioral monitoring flagging agent actions outside normal operational patterns (e.g., creating new files when tasked with review)
- Secrets access logging correlating agent identity with secret retrieval events
- Regular privilege review cycles specifically for non-human identities in CI/CD pipelines

## Mitigations

- Apply least-privilege principles to all AI agents: read-only by default, write access only for specific approved operations
- Separate agent credentials from human credentials with distinct permission boundaries
- Require human approval for any agent action that creates files, modifies CI configuration, or accesses secrets
- Implement token scoping that limits agent access to the specific repository, branch, and file paths relevant to each task

## Related Mappings

- **CWE-250**: Execution with Unnecessary Privileges
- **CWE-269**: Improper Privilege Management
- **OWASP LLM06**: Excessive Agency

## Severity Rationale

Ranked CRITICAL because agent privilege compromise provides direct access to the software supply chain. The combination of over-privileged agents and prompt injection creates a reliable attack chain. Most organizations have not yet audited non-human identity permissions in their CI/CD infrastructure.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
