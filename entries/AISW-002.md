# AISW-002: Prompt-Injected Coding Agent Execution

| Field | Value |
|-------|-------|
| **Identifier** | AISW-002 |
| **Rank** | #2 of 25 |
| **Severity** | CRITICAL |

---

## Description

Coding agents that consume untrusted context — repository READMEs, issue descriptions, pull request comments, documentation pages, or retrieved code snippets — are susceptible to prompt injection that redirects their code generation or execution behavior. The agent writes, modifies, or executes attacker-chosen code while operating under developer-granted privileges.

The attack surface expands with every new context source the agent consumes. Current prompt injection defenses remain brittle, and the consequences of successful injection against a coding agent with write access to production repositories are categorically worse than injection against a chatbot.

## Exploit Scenario

An attacker submits a pull request to an open-source project containing a markdown comment in the PR description with hidden instructions: a unicode-encoded directive telling the reviewing agent to add an exfiltration line to the CI configuration.

The organization's AI code review bot processes the PR description as context, follows the injected instruction, and approves a modified CI step that pipes environment secrets to an external endpoint. The change appears as a minor formatting update in the diff.

## Detection Methods

- Input sanitization layers that strip or flag instruction-like patterns in all agent context sources
- Diff auditing that compares agent-proposed changes against the scope of the original task description
- Behavioral monitoring of agent actions: flag any file modifications outside the declared task scope
- Canary tokens in CI secrets that alert on any external transmission attempt

## Mitigations

- Treat all repository content, issues, PRs, and documentation as untrusted input to coding agents
- Implement strict scope boundaries: agents may only modify files explicitly named in the task
- Require human approval for any agent action that touches CI/CD configuration, secrets, or deployment files
- Run agents in sandboxed environments with no network egress and read-only access to secrets

## Related Mappings

- **CWE-94**: Improper Control of Generation of Code
- **CWE-77**: Command Injection
- **OWASP LLM01**: Prompt Injection
- **OWASP LLM06**: Excessive Agency

## Severity Rationale

Ranked #2 because coding agents increasingly operate with write access to production repositories and CI/CD pipelines. A successful injection converts a trusted automation tool into an insider threat. The attack surface grows with every new context source the agent consumes, and current prompt injection defenses remain brittle.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
