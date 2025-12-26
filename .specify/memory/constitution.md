<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution)
- Added sections: All principles and governance sections
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ reviewed
- Follow-up TODOs: None
-->
# AI/Spec-Driven Book Creation with Integrated RAG Chatbot Constitution

## Core Principles

### I. Specification-First Development
Every feature and component must be defined through comprehensive specifications before implementation begins. All technical claims must be verifiable from official documentation and all architecture decisions must be justified and documented. This ensures reproducible and maintainable code.

### II. Factual Accuracy and Verifiability
All technical content and claims must be grounded in verified official documentation. Code examples must be runnable and reproducible. No assumptions or unverified information is acceptable in the book content or system implementation.

### III. RAG Integrity and Hallucination Prevention
The RAG chatbot must strictly answer questions based only on retrieved context from the book content or user-selected text. Responses must cite retrieved context and clearly indicate when information is not found. No hallucinations are permitted under any circumstances.

### IV. Modular and Maintainable System Design
The system architecture must be modular, with clear separation of concerns between frontend (Docusaurus), backend API (FastAPI), vector database (Qdrant Cloud), and metadata storage (Neon Postgres). Components must be independently testable and maintainable.

### V. Performance and Latency Optimization
All system components must maintain low-latency responses suitable for web embedding. Vector search operations, API calls, and UI interactions must be optimized for user experience. Performance budgets and SLOs must be defined and monitored.

### VI. Reproducibility and Documentation Standards
All code, prompts, and system architecture must be completely reproducible through documentation. Markdown-first content with clear code snippet explanations, diagrams for system architecture, and step-by-step setup guides are mandatory.

## Technology and Architecture Constraints

The system must utilize the specified technology stack: Docusaurus for book authoring, FastAPI for backend API, Qdrant Cloud Free Tier for vector search, Neon Serverless Postgres for metadata storage, and OpenAI Agents/ChatKit SDKs for AI orchestration. All hosting must be compatible with GitHub Pages for frontend and cloud service free tiers for backend components.

## Development Workflow

All development must follow Spec-Kit Plus and Claude Code practices. Every implementation task must trace back to specifications. Code reviews must verify compliance with all principles, particularly RAG integrity and factual accuracy. All changes must be tested and validated against the acceptance criteria before merging.

## Governance

This constitution supersedes all other development practices and must be strictly followed. All pull requests and code reviews must verify compliance with these principles. Any architectural changes that affect core principles require formal amendment documentation and approval. All team members must acknowledge and follow these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2025-12-26
