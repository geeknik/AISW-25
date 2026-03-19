# AISW-025: Reviewer Automation Bias

| Field | Value |
|-------|-------|
| **Identifier** | AISW-025 |
| **Rank** | #25 of 25 |
| **Severity** | MEDIUM |

---

## Description

Human code reviewers apply less scrutiny to AI-generated code than to human-written code. AI output appears well-structured, consistently styled, and accompanied by coherent explanations, creating a trust signal that reduces the reviewer's critical evaluation.

This is not a single exploitable vulnerability but a systemic amplifier of all other AISW entries. Every weakness in this catalog is more likely to reach production when reviewers assume AI-generated code is correct by default. The weakness compounds: as AI generates more code, review fatigue increases, and the acceptance threshold drops further.

## Exploit Scenario

This entry does not describe a single exploit but a systemic condition. Studies show that developers who use AI assistants produce code with more vulnerabilities that passes review at higher rates than manually written code.

Every other entry in this catalog — from authorization synthesis failures to patch placebos to diff inflation — is more likely to survive review and ship to production under automation bias. The dangerous period is not when AI is first adopted but 6–12 months later, when review discipline has eroded but the generation pipeline has not materially improved.

## Detection Methods

- Review metrics tracking approval latency, comment density, and rejection rates for AI-assisted vs. manual PRs
- Periodic injection of known-vulnerable AI-generated code into review queues to test reviewer vigilance
- Mandatory review checklists with security-specific items that must be explicitly addressed, not just acknowledged
- Post-incident analysis tracking whether production vulnerabilities were present in reviewed AI-generated PRs

## Mitigations

- Train reviewers specifically on AI-generated code weaknesses and the patterns in this catalog
- Require that AI-generated PRs are explicitly labeled and subject to enhanced review protocols
- Implement mandatory security-focused automated analysis that runs independently of human review
- Rotate reviewers and assign security-trained reviewers to AI-heavy PRs to prevent habituation
- Establish organizational culture that treats AI output as draft-quality by default, not production-ready

## Related Mappings

- **N/A**: No direct CWE. Process and human-factors weakness that amplifies all technical CWEs.

## Severity Rationale

Ranked #25 not because it is least important but because it is a meta-weakness: it does not create vulnerabilities directly but dramatically increases the probability that all other weaknesses survive to production. Addressing automation bias is a prerequisite for effective defense against every other entry in this catalog.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
