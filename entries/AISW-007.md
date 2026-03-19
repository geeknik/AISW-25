# AISW-007: Test Suite Laundering

| Field | Value |
|-------|-------|
| **Identifier** | AISW-007 |
| **Rank** | #7 of 25 |
| **Severity** | HIGH |

---

## Description

AI-generated test suites encode the bug as expected behavior, making vulnerable code appear verified. The model generates tests that assert the code's actual output rather than its intended secure behavior. Negative test cases are absent or trivial. The result is a green CI pipeline that provides false assurance while the underlying vulnerability persists.

This is particularly dangerous when the same AI generates both the implementation and its tests, because the model's understanding of "correct" behavior is derived from the same flawed reasoning that produced the bug.

## Exploit Scenario

A developer generates both a user registration endpoint and its test suite using an AI assistant. The endpoint fails to validate email format, allowing injection of control characters. The generated test suite tests `register("user@example.com")` and asserts success — but never tests `register("user@example.com\r\nBCC:attacker@evil.com")`.

Worse, the AI generates a test for duplicate registration that inadvertently asserts the control-character email is "valid." The test suite shows 100% pass rate and 94% coverage. The header injection vulnerability ships to production.

## Detection Methods

- Mutation testing that verifies test suites detect injected faults in security-critical code paths
- Test review requiring explicit negative cases for every input validation function
- Coverage analysis specifically targeting security-relevant branch conditions, not just line coverage
- Independent test generation from security specifications, compared against AI-generated test assertions

## Mitigations

- Maintain a separate, human-authored security test suite that is never overwritten by AI-generated tests
- Require mutation testing scores above threshold for all security-critical modules as a CI gate
- Mandate adversarial test cases (injection, overflow, boundary) for every input-handling function
- Separate the test author from the code author: if AI wrote the code, a human writes the security tests, or vice versa

## Related Mappings

- **CWE-20**: Improper Input Validation
- **CWE-1164**: Irrelevant Code

## Severity Rationale

Ranked HIGH because test laundering defeats the primary quality gate in modern development. Organizations that trust CI pass rates as security signals will ship vulnerable code with high confidence. The failure is systemic: it corrupts the feedback loop between development and assurance.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
