# AISW-011: RAG-Contaminated Engineering Guidance

| Field | Value |
|-------|-------|
| **Identifier** | AISW-011 |
| **Rank** | #11 of 25 |
| **Severity** | HIGH |

---

## Description

Retrieval-augmented generation (RAG) systems that feed internal documentation, wiki pages, Slack threads, or ticket comments into coding assistants propagate insecure advice when the retrieved context contains outdated, incorrect, or intentionally poisoned engineering guidance.

The model treats retrieved content as authoritative, amplifying bad advice into generated code. The attack surface includes every internal document, ticket, and wiki page that has ever existed in the organization's knowledge base.

## Exploit Scenario

An internal wiki page from 2019 documents a database connection pattern using plaintext credentials in environment variables with no encryption. A RAG-augmented coding assistant retrieves this page when a developer asks how to connect to the company's database.

The assistant generates code following the outdated pattern, complete with plaintext credential handling. The developer, seeing that the code references internal documentation, trusts it as current practice. The pattern propagates to three new services before security review catches it.

## Detection Methods

- Metadata filtering in RAG pipelines that deprioritizes or excludes documents older than a defined threshold
- Content tagging systems that mark superseded documentation and prevent retrieval for code generation
- Audit logging of which documents are retrieved for each AI-assisted coding session
- Periodic review of top-retrieved documents for security accuracy and currency

## Mitigations

- Implement document lifecycle management that automatically deprecates and removes outdated engineering guidance
- Tag all internal documentation with security review dates and exclude unreviewed content from RAG retrieval
- Maintain a curated, security-reviewed knowledge base as the primary retrieval source for coding assistants
- Enable developers to flag and dispute retrieved guidance that conflicts with current security practices

## Related Mappings

- **CWE-348**: Use of Less Trusted Source
- **OWASP LLM08**: Vector and Embedding Weaknesses

## Severity Rationale

Ranked HIGH because RAG systems are the primary mechanism for injecting organizational context into AI coding, and most organizations have not implemented retrieval quality controls. The attack surface includes every internal document, ticket, and wiki page that has ever existed.

---

*AISW-25 v0.1 — Aether Systems Labs, Inc. — CC BY-SA 4.0*
