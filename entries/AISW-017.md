# AISW-017: Async and Concurrency Boilerplate Hazards

| Field | Value |
|-------|-------|
| **Identifier** | AISW-017 |
| **Rank** | #17 of 25 |
| **Severity** | MEDIUM |

---

## Description

AI-generated concurrent and asynchronous code contains race conditions, missed locks, double-free vulnerabilities, time-of-check-to-time-of-use (TOCTOU) windows, deadlocks, and unsafe shared-state mutations.

Models generate syntactically correct concurrent code that works under low contention but fails under production load or adversarial timing. AI models are particularly bad at concurrency because correct patterns are underrepresented relative to incorrect ones in training data.

## Exploit Scenario

An AI assistant generates a rate limiter using a shared Redis counter. The generated code reads the current count, checks it against the limit, and increments it — in three separate operations without atomic guarantees. Under normal load, the race window is negligible.

An attacker sends a burst of concurrent requests timed to exploit the TOCTOU window between the check and the increment, bypassing the rate limit and launching a brute-force attack against the authentication endpoint the rate limiter was supposed to protect.

## Detection Methods

- Concurrency-focused static analysis tools (ThreadSanitizer, go race detector) run as CI gates
- Load testing under high contention specifically targeting shared-state operations
- Code review checklists requiring atomic operations for all check-then-act patterns
- Behavioral testing that verifies rate limiters, locks, and counters under concurrent stress

## Mitigations

- Use atomic operations (INCR, SETNX, CAS) for all shared-state modifications; never separate read-check-write
- Provide pre-approved concurrency primitives as organizational libraries; prohibit ad-hoc locking patterns
- Require concurrent code to be load-tested under adversarial conditions before deployment
- Use Rust, Go, or other languages with compile-time concurrency safety guarantees where possible

## Related Mappings

- **CWE-362**: Concurrent Execution Using Shared Resource with Improper Synchronization
- **CWE-367**: TOCTOU Race Condition

## Severity Rationale

Ranked MEDIUM because concurrency bugs require specific conditions to exploit, but when exploitable, they often bypass security controls entirely. AI models are particularly bad at concurrency because correct patterns are underrepresented relative to incorrect ones in training data.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
