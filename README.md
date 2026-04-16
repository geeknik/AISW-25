# AISW-25: AI-Induced Software Weaknesses

**Top 25 Catalog of Failure Amplifiers in AI-Assisted Software Development**

[![Version](https://img.shields.io/badge/version-0.1-blue)]() [![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0-green)](LICENSE) [![Status](https://img.shields.io/badge/status-pre--release%20draft-orange)]()

---

## The Problem

Existing security frameworks ask the wrong question about AI-generated code.

**OWASP LLM Top 10** asks: *What can go wrong with an LLM application?*
**MITRE CWE Top 25** asks: *What are the most dangerous software weaknesses?*

Neither asks: **What weakness patterns become materially more common, cheaper to mass-produce, and harder to detect once AI code generation becomes normal?**

AISW-25 answers that question.

The dangerous unit in AI-assisted development is no longer the vulnerable line of code. It is the **generation pipeline**: model behavior, retrieved context, agent permissions, trust boundaries, and human over-trust interacting simultaneously. A single insecure pattern emitted by a model can propagate across dozens of services, templates, and internal libraries before anyone names the bug.

## What This Is

A structured, citable catalog of 25 AI-induced software weakness patterns, each containing:

- **Identifier** (AISW-001 through AISW-025) — stable references for bug trackers, audits, and compliance docs
- **Description** — precise root cause in AI generation behavior and propagation mechanism
- **Exploit Scenario** — concrete, realistic attack narrative against production systems
- **Detection Methods** — specific tooling, analysis, and review practices
- **Mitigations** — actionable countermeasures for immediate implementation
- **CWE/OWASP Mappings** — cross-references to established taxonomies
- **Severity Rationale** — ranking justification based on propagation velocity, detection difficulty, blast radius, and AI amplification factor

## Severity Distribution

| Severity | Count | Scope |
|----------|-------|-------|
| **CRITICAL** | 5 | Full data breach, supply chain compromise, or RCE from a single instance |
| **HIGH** | 9 | Significant impact; systematically evades standard review |
| **MEDIUM** | 11 | Exploitable under specific conditions or as an amplifier of other weaknesses |

## The Top 25 at a Glance

| # | ID | Name | Severity |
|---|-----|------|----------|
| 1 | AISW-001 | Authorization Logic Synthesis Failure | CRITICAL |
| 2 | AISW-002 | Prompt-Injected Coding Agent Execution | CRITICAL |
| 3 | AISW-003 | Dependency Confabulation and Typosquat Intake | CRITICAL |
| 4 | AISW-004 | Insecure Default Infrastructure Generation | CRITICAL |
| 5 | AISW-005 | Secret Reintroduction by Completion | HIGH |
| 6 | AISW-006 | Hallucinated Security API Usage | HIGH |
| 7 | AISW-007 | Test Suite Laundering | HIGH |
| 8 | AISW-008 | Unsafe Output-to-Tool Bridging | HIGH |
| 9 | AISW-009 | Stale Vulnerable Pattern Regeneration | HIGH |
| 10 | AISW-010 | Excessive Agent Privilege in CI/CD | CRITICAL |
| 11 | AISW-011 | RAG-Contaminated Engineering Guidance | HIGH |
| 12 | AISW-012 | Patch Placebo | HIGH |
| 13 | AISW-013 | Unsafe Deserialization by Scaffold | HIGH |
| 14 | AISW-014 | Cross-Boundary Validation Omission | MEDIUM |
| 15 | AISW-015 | Logging-Induced Sensitive Data Exposure | HIGH |
| 16 | AISW-016 | Spec Overreach Privilege Creep | MEDIUM |
| 17 | AISW-017 | Async and Concurrency Boilerplate Hazards | MEDIUM |
| 18 | AISW-018 | Resource-Exhaustion and Cost Bombs | MEDIUM |
| 19 | AISW-019 | Vulnerable Migration and Rollback Scripts | MEDIUM |
| 20 | AISW-020 | Sanitizer Mismatch Across Languages | MEDIUM |
| 21 | AISW-021 | Review Evasion by Diff Inflation | MEDIUM |
| 22 | AISW-022 | Auto-Remediation Regression | MEDIUM |
| 23 | AISW-023 | Faux Reproducibility in Build Pipelines | MEDIUM |
| 24 | AISW-024 | Policy-to-Code Drift | MEDIUM |
| 25 | AISW-025 | Reviewer Automation Bias | MEDIUM |

## Why This Matters Now

The old threat model assumes developers create bugs one commit at a time. The AI-induced threat model assumes bugs are **synthesized in batches, justified by plausible prose, wrapped in passing tests, and merged through review fatigue.**

Five systemic dynamics make this urgent:

1. **Batch propagation.** One flawed pattern instantiates across an entire service mesh within a sprint.
2. **Pipeline as attack surface.** The generation pipeline — model, retrieval context, agent permissions, trust boundaries — is the new vulnerability surface.
3. **Statistical inevitability.** Models emit the most statistically likely completion, which for security-sensitive patterns is often the insecure one.
4. **Review collapse.** AI-generated code's surface quality reduces the scrutiny reviewers apply.
5. **Compounding trust.** Each successfully merged AI PR lowers the review threshold. The most dangerous period is 6–12 months after adoption, when review discipline has eroded.

## How to Use This

**Security training.** Use the exploit scenarios as training material. Each one is concrete, memorable, and maps to a real production failure mode.

**Code review checklists.** Derive checklist items from the detection methods. Reviewers should have AISW-specific items for AI-generated PRs.

**CI/CD gates.** Implement detection methods as automated checks. Prioritize CRITICAL and HIGH entries for immediate enforcement.

**Threat modeling.** Include AISW entries when modeling systems that use AI-assisted code generation.

**Audit and compliance.** Reference AISW identifiers in audit findings. The identifier scheme is designed for formal citation.

**Vendor evaluation.** Test AI coding tools against the exploit scenarios. Evaluate tool performance against detection and mitigation recommendations.

## Repository Structure

```
.
├── README.md
├── LICENSE                          # CC BY-SA 4.0
├── CONTRIBUTING.md
├── .github/
│   └── workflows/
│       └── validate.yml             # Catalog and generator validation in CI
├── entries/
│   ├── AISW-001.md                  # Individual entry files (structured markdown)
│   ├── AISW-002.md
│   ├── ...
│   └── AISW-025.md
├── mappings/
│   ├── cwe-cross-reference.csv      # Machine-readable CWE mappings, including N/A rows
│   └── owasp-cross-reference.csv    # Machine-readable OWASP mappings, including N/A rows
├── tests/
│   └── test_catalog_integrity.py    # Regression tests for catalog integrity
└── tools/
    └── checklist_generator.py       # Generate review checklists from entries
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

We welcome contributions in these areas:

- **New exploit scenarios** for existing entries based on real-world incidents
- **Detection method improvements** with tooling references and configuration examples
- **Mitigation refinements** with implementation guides for specific tech stacks
- **New entry proposals** for AI-induced weakness patterns not yet cataloged
- **CWE/OWASP mapping corrections** and additional cross-references
- **Translations** into other languages

All contributions are reviewed by maintainers and must include evidence or reasoning for proposed changes. This is a security specification, not a wiki — precision matters.

## Citing This Work

```
Aether Systems Labs. "AISW-25: AI-Induced Software Weaknesses —
Top 25 Catalog of Failure Amplifiers in AI-Assisted Software Development."
Version 0.1, March 2026. https://github.com/geeknik/aisw-25
```

BibTeX:
```bibtex
@techreport{aisw25,
  title     = {AISW-25: AI-Induced Software Weaknesses},
  author    = {{Aether Systems Labs}},
  year      = {2026},
  month     = {3},
  version   = {0.1},
  url       = {https://github.com/geeknik/aisw-25},
  note      = {Top 25 Catalog of Failure Amplifiers in AI-Assisted Software Development}
}
```

## Acknowledgments

*This section will list reviewers and contributors who provided feedback on the pre-release draft.*

## License

This work is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

You are free to share and adapt this material for any purpose, including commercial use, provided you give appropriate credit and distribute derivative works under the same license.

---

**Maintained by [Aether Systems Labs, Inc](https://aetherai.systems)**
