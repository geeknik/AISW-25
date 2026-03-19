# AISW-018: Resource-Exhaustion and Cost Bombs

| Field | Value |
|-------|-------|
| **Identifier** | AISW-018 |
| **Rank** | #18 of 25 |
| **Severity** | MEDIUM |

---

## Description

AI-generated code contains unbounded loops, unlimited retries with exponential backoff that never caps, fan-out operations with no concurrency limits, regex patterns vulnerable to catastrophic backtracking, or parser configurations that accept arbitrarily nested structures.

These patterns create denial-of-service vulnerabilities and cloud cost explosions under adversarial input. AI models routinely generate unbounded patterns because training data demonstrations are optimized for simplicity, not resilience.

## Exploit Scenario

A developer uses an AI assistant to generate a webhook processor that retries failed deliveries with exponential backoff. The generated code has no maximum retry count and no circuit breaker. An attacker sends a webhook payload to an endpoint that always returns a 500 error.

The processor retries indefinitely with increasing delays, spawning queued jobs that consume worker capacity and database connections. Within hours, the job queue contains millions of retry entries, the worker pool is exhausted, and legitimate webhook processing halts.

## Detection Methods

- Static analysis rules flagging unbounded loops, unlimited retry configurations, and missing circuit breakers
- Cost monitoring with anomaly detection alerting on unexpected cloud spend increases
- Load testing with adversarial inputs specifically targeting retry, fan-out, and parsing paths
- Regex static analysis tools (e.g., rxxr2) checking for catastrophic backtracking patterns

## Mitigations

- Enforce maximum retry counts, concurrency limits, and circuit breakers as mandatory patterns for all async operations
- Implement budget-aware resource controls that cap cloud spend and worker allocation per service
- Require all AI-generated regex patterns to be tested against ReDoS payloads before deployment
- Set hard limits on request size, nesting depth, and processing time at the infrastructure layer

## Related Mappings

- **CWE-400**: Uncontrolled Resource Consumption
- **CWE-1333**: Inefficient Regular Expression Complexity
- **OWASP LLM04**: Denial of Service

## Severity Rationale

Ranked MEDIUM because resource exhaustion typically causes availability loss rather than data breach, but cloud cost bombs can have significant financial impact. AI models routinely generate unbounded patterns because training data demonstrations are optimized for simplicity, not resilience.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
