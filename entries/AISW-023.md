# AISW-023: Faux Reproducibility in Build Pipelines

| Field | Value |
|-------|-------|
| **Identifier** | AISW-023 |
| **Rank** | #23 of 25 |
| **Severity** | MEDIUM |

---

## Description

AI-generated build configurations, Dockerfiles, and CI/CD pipelines use unpinned dependencies, mutable base images, unverified external artifacts, and no integrity checks. Builds appear reproducible in testing but can produce different — and potentially compromised — outputs on each run.

AI models consistently generate unpinned configurations because pinned examples are underrepresented in training data. The resulting builds silently trust mutable external artifacts.

## Exploit Scenario

An AI generates a Dockerfile with `FROM node:latest` and `RUN npm install` without a lockfile. The image builds successfully in testing. Months later, a compromised npm package is published under the same name, and `node:latest` updates to include a security patch that changes default behavior.

The next build pulls both the compromised package and the changed base image, producing a container that functions correctly but contains a backdoor. No integrity check exists to detect the difference.

## Detection Methods

- Build reproducibility testing that compares outputs across multiple builds and flags any differences
- Dockerfile linting requiring pinned base images (digest, not tag) and lockfile-based installs
- Software Bill of Materials (SBOM) generation and comparison across builds
- Integrity verification of all external artifacts pulled during build, with hash pinning

## Mitigations

- Pin all base images by digest, all dependencies by exact version with hash verification
- Require lockfiles for all package managers and verify lockfile integrity in CI
- Implement reproducible build verification that compares build outputs and alerts on drift
- Use private artifact registries with integrity scanning; never pull directly from public registries in production builds

## Related Mappings

- **CWE-1357**: Reliance on Insufficiently Trustworthy Component
- **CWE-829**: Inclusion of Functionality from Untrusted Control Sphere

## Severity Rationale

Ranked MEDIUM because build pipeline compromises are high-impact but require supply chain positioning by the attacker. AI models consistently generate unpinned configurations because pinned examples are underrepresented in training data.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
