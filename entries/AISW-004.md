# AISW-004: Insecure Default Infrastructure Generation

| Field | Value |
|-------|-------|
| **Identifier** | AISW-004 |
| **Rank** | #4 of 25 |
| **Severity** | CRITICAL |

---

## Description

AI-generated infrastructure-as-code (Terraform, Kubernetes manifests, CloudFormation, IAM policies, CI/CD configurations) ships with permissive defaults that are appropriate for development but catastrophic in production. Models optimize for "it works" over "it's secure," producing public S3 buckets, wildcard IAM policies, disabled network policies, and privileged container configurations that survive to deployment because they function correctly in testing.

Unlike application code where bugs typically affect a single endpoint, infrastructure misconfigurations expose entire environments, accounts, and data stores.

## Exploit Scenario

A platform team asks a coding assistant to generate Terraform for a new AWS microservice. The generated IAM role uses `Action: "*"` and `Resource: "*"` because the model prioritizes ensuring the service works without permission errors. The S3 bucket is created without `block_public_access`. The security group allows inbound 0.0.0.0/0 on the application port.

The configuration passes `terraform plan` and deploys successfully. Three weeks later, a misconfigured application endpoint exposes the S3 bucket URL, and the bucket — now containing customer PII — is indexed by automated scanners.

## Detection Methods

- IaC scanning tools (tfsec, checkov, kics) integrated as mandatory CI gates on all infrastructure PRs
- Policy-as-code enforcement (OPA/Rego, Sentinel) that rejects wildcard permissions and public access patterns
- Automated drift detection comparing deployed infrastructure against hardened baselines
- Periodic access review audits flagging over-provisioned IAM roles and security groups

## Mitigations

- Maintain hardened IaC templates as the only approved starting point; AI output must be diffed against these baselines
- Enforce least-privilege IAM policies through automated policy boundary enforcement at the organization level
- Require all AI-generated infrastructure code to pass policy-as-code gates before merge, with zero exceptions
- Implement default-deny network policies and require explicit justification for any inbound access rules

## Related Mappings

- **CWE-276**: Incorrect Default Permissions
- **CWE-732**: Incorrect Permission Assignment for Critical Resource
- **OWASP LLM05**: Supply Chain Vulnerabilities

## Severity Rationale

Ranked #4 because infrastructure misconfigurations are the leading cause of cloud breaches, and AI generation makes permissive defaults the path of least resistance. Unlike application bugs, infrastructure flaws often persist undetected for weeks or months and expose entire environments rather than single endpoints.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
