# AISW-013: Unsafe Deserialization by Scaffold

| Field | Value |
|-------|-------|
| **Identifier** | AISW-013 |
| **Rank** | #13 of 25 |
| **Severity** | HIGH |

---

## Description

Boilerplate generators, project scaffolds, and code templates produced by AI include dangerous deserialization patterns: Python's `pickle.loads()` on untrusted input, Java's `ObjectInputStream` without filtering, PHP's `unserialize()`, or YAML `load()` instead of `safe_load()`.

These patterns persist because they are the most common in training data and require fewer lines of code than safe alternatives. Every new service scaffolded with AI begins with the vulnerability baked into its foundation.

## Exploit Scenario

A developer uses an AI assistant to scaffold a Python web application with Redis-based session storage. The generated code uses `pickle.loads()` to deserialize session data from Redis. An attacker who gains write access to the Redis instance (through a separate SSRF vulnerability) injects a crafted pickle payload into a session key.

When the application loads the session, the pickle payload executes arbitrary code with the application's privileges, achieving remote code execution.

## Detection Methods

- SAST rules specifically banning `pickle.loads`, `yaml.load`, `ObjectInputStream`, and `unserialize` on untrusted data
- Scaffold auditing tools that scan project templates for known dangerous patterns before first deployment
- Import analysis flagging dangerous deserialization functions in any module that handles external data
- Organizational linting rules that require safe alternatives (e.g., `yaml.safe_load`, `json.loads`) and block unsafe ones

## Mitigations

- Ban unsafe deserialization functions at the organizational linting level with no override mechanism
- Provide pre-approved serialization libraries as the only permitted option for handling external data
- Replace all `pickle`/`yaml.load`/`unserialize` usage with JSON or protocol buffers for data interchange
- If binary serialization is required, enforce allow-list filtering on deserialized types

## Related Mappings

- **CWE-502**: Deserialization of Untrusted Data
- **OWASP A08**: Software and Data Integrity Failures

## Severity Rationale

Ranked HIGH because deserialization vulnerabilities frequently lead to remote code execution, the highest-impact exploit class. AI scaffolding makes these patterns the default starting point for new projects, meaning every new service begins with the vulnerability baked in.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
