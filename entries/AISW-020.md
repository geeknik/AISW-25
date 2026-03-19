# AISW-020: Sanitizer Mismatch Across Languages

| Field | Value |
|-------|-------|
| **Identifier** | AISW-020 |
| **Rank** | #20 of 25 |
| **Severity** | MEDIUM |

---

## Description

AI-generated code applies escaping or validation logic appropriate for one language or runtime context but uses it in a different sink. HTML escaping applied to SQL contexts, URL encoding used where shell escaping is needed, or JavaScript sanitization applied to server-side template injection sinks.

The model selects sanitization based on pattern matching rather than understanding the specific sink semantics. In polyglot applications, this mismatch is particularly common and dangerous.

## Exploit Scenario

A developer builds a polyglot application with a Python backend and JavaScript frontend. The AI generates server-side code that HTML-escapes user input before inserting it into a SQL query, believing it has "sanitized" the input. The HTML escaping does not prevent SQL injection because `'` is not an HTML special character.

The attacker injects SQL through a field that the developer believes is safe because "it's sanitized."

## Detection Methods

- Taint analysis tracking data flow from input to specific sink type, verifying sink-appropriate sanitization
- Code review training on context-specific sanitization requirements (SQL vs. HTML vs. shell vs. LDAP)
- SAST rules that flag sanitization function calls and verify they match the downstream sink type
- Integration tests injecting sink-specific payloads at every validated input point

## Mitigations

- Use parameterized interfaces for every sink type; never rely on manual sanitization
- Implement context-aware sanitization libraries that select the correct escaping based on the declared sink
- Prohibit raw string manipulation for any data flowing to execution sinks; require ORM/template-engine/prepared-statement patterns
- Document the sanitization requirements for each sink type in organizational security guidelines

## Related Mappings

- **CWE-116**: Improper Encoding or Escaping of Output
- **CWE-838**: Inappropriate Encoding for Output Context

## Severity Rationale

Ranked MEDIUM because exploitation requires that the attacker identifies the sanitizer-sink mismatch, which is non-obvious. However, AI models routinely confuse sanitization contexts, making this a common pattern in generated code.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
