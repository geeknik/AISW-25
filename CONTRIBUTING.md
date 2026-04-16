# Contributing to AISW-25

Thank you for your interest in improving the AISW-25 catalog. This is a security specification. Contributions are held to a high standard of precision, evidence, and actionability.

## What We Accept

### Exploit Scenario Additions
New or improved exploit scenarios for existing entries. Must be:
- Concrete and reproducible (no hypothetical hand-waving)
- Mapped to a realistic production environment
- Distinct from the existing scenario for that entry

### Detection Method Improvements
Specific tooling, configurations, or analysis techniques. Must include:
- Tool name and version (or class of tool if vendor-agnostic)
- Configuration example or rule definition where applicable
- Evidence that the method detects the weakness pattern described in the entry

### Mitigation Refinements
Implementation-specific countermeasures. Must include:
- Target technology stack or platform
- Code example or configuration snippet
- Explanation of why the mitigation addresses the root cause, not just the symptom

### New Entry Proposals
Proposals for AI-induced weakness patterns not yet cataloged. Must include:
- All fields used in the current entry template in `entries/AISW-001.md` through `entries/AISW-025.md`
- Evidence that the pattern is materially amplified by AI code generation
- At least one concrete exploit scenario
- Proposed CWE/OWASP mappings with justification

### CWE/OWASP Mapping Corrections
Corrections or additions to cross-reference mappings. Must include:
- The specific mapping being corrected or added
- CWE/OWASP identifier with rationale for the mapping
- Use `N/A` in the identifier column when an entry is intentionally unmapped but still needs machine-readable coverage
- Explanation of why the current mapping is incorrect (for corrections)

## What We Do Not Accept

- Entries that describe general software weaknesses without a clear AI amplification mechanism
- Mitigations that amount to "be more careful" or "review more thoroughly" without specific process changes
- Marketing or promotional content for specific security products
- Speculative weakness patterns without evidence or concrete exploit scenarios
- Changes that reduce the specificity or actionability of existing entries

## Process

1. **Open an issue first.** Describe your proposed change before submitting a PR. This prevents wasted effort on contributions that don't align with the catalog's scope.
2. **One change per PR.** Keep contributions atomic. A new exploit scenario for AISW-007 is one PR. A mapping correction for AISW-012 is another.
3. **Follow the existing format exactly.** Entries, detection methods, and mitigations have a specific structure. Match it.
4. **Cite your sources.** If referencing a CVE, paper, incident report, or tool, include the reference.
5. **Maintainer review.** All contributions are reviewed by maintainers for accuracy, precision, and alignment with the catalog's scope.

## Style Guidelines

- Write in declarative, precise language. Avoid hedging ("might," "could potentially," "in some cases").
- Use present tense for descriptions ("The model generates...") and past tense for exploit scenarios ("The attacker submitted...").
- Specify concrete tools, configurations, and techniques. "Use static analysis" is insufficient. "Run Semgrep rule `python.lang.security.audit.dangerous-pickle-import`" is actionable.
- Keep entries self-contained. A reader should understand the weakness, its exploitation, and its countermeasures from the entry alone.

## Code of Conduct

Contributors are expected to engage professionally and constructively. This is a technical security project. Debates about entry ranking, severity classification, and mitigation effectiveness are welcome and expected. Personal attacks, dismissive language, and bad-faith engagement are not.

## Questions

Open an issue tagged `question` for clarification on scope, format, or contribution guidelines.
