# AISW-016: Spec Overreach Privilege Creep

| Field | Value |
|-------|-------|
| **Identifier** | AISW-016 |
| **Rank** | #16 of 25 |
| **Severity** | MEDIUM |

---

## Description

AI-generated code over-implements the requested feature by adding capabilities not specified in the requirements: admin endpoints, debug routes, configuration interfaces, broader API scopes, or elevated permission requests.

The model generates these additions because they are common in the training data patterns associated with the requested feature type. The result is undocumented, unauthenticated attack surface that was never specified, never reviewed for security, and never tested.

## Exploit Scenario

A developer requests a user profile endpoint. The AI generates the endpoint along with an undocumented `/admin/users` route that lists all users with full profile details, because the training data commonly pairs user endpoints with admin CRUD operations. The admin route has no authentication because it was never specified in the requirements and was never reviewed.

An attacker discovers the route through directory brute-forcing and exfiltrates the full user database.

## Detection Methods

- Diff review comparing generated endpoints against the original feature specification
- Route scanning tools that detect undocumented endpoints in the application routing table
- Automated API inventory that flags endpoints not present in the API specification or documentation
- PR review checklists requiring developers to justify every new route, scope, and permission in generated code

## Mitigations

- Require generated code to be scoped strictly to the feature specification; delete unrequested capabilities before merge
- Implement API gateway rules that reject requests to undocumented endpoints by default
- Run automated endpoint discovery in staging environments and compare against declared API surface
- Enforce the principle that any new endpoint requires explicit security review and documentation

## Related Mappings

- **CWE-269**: Improper Privilege Management
- **CWE-749**: Exposed Dangerous Method or Function

## Severity Rationale

Ranked MEDIUM because the vulnerability requires that the overreach code reaches production undetected, which is less likely in organizations with route-level review. However, in fast-moving teams with AI-heavy workflows, undocumented routes are commonly overlooked.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
