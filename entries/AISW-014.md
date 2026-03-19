# AISW-014: Cross-Boundary Validation Omission

| Field | Value |
|-------|-------|
| **Identifier** | AISW-014 |
| **Rank** | #14 of 25 |
| **Severity** | MEDIUM |

---

## Description

AI-generated code validates input at one entry point (typically the API handler) but omits equivalent validation at other trust boundary crossings: background workers processing queue messages, CLI tools consuming the same data, admin endpoints, webhook receivers, and inter-service communication.

The model generates validation for the context it sees but has no awareness of other paths to the same data processing logic. Each module is generated independently without cross-cutting architectural context.

## Exploit Scenario

An API endpoint validates that a `quantity` field is a positive integer. The same order processing logic is invoked by a background worker consuming messages from a message queue. The AI-generated worker code does not validate the `quantity` field because the developer only asked for API validation.

An attacker who can inject a message into the queue (through a separate authorization flaw) sends a negative quantity, causing the system to issue a refund for an order that was never placed.

## Detection Methods

- Data flow analysis mapping all entry points to shared business logic and verifying validation at each boundary
- Architectural review identifying all consumers of shared data models and checking for consistent validation
- Integration tests that send invalid data through every entry point, not just the primary API
- Centralized validation schema enforcement at the data model layer rather than the handler layer

## Mitigations

- Implement validation at the data model or domain layer so it applies regardless of entry point
- Require schema validation at every trust boundary, enforced by shared validation middleware
- Document all entry points for each data processing function and require test coverage for each
- Use contract-based interfaces (e.g., protocol buffers, JSON Schema) that enforce validation at serialization boundaries

## Related Mappings

- **CWE-20**: Improper Input Validation
- **CWE-602**: Client-Side Enforcement of Server-Side Security

## Severity Rationale

Ranked MEDIUM because the vulnerability requires a secondary access path to exploit, but the pattern is extremely common in AI-generated codebases where each module is generated independently without cross-cutting context.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
