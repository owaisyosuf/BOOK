---
id: 1
title: initial-constitution
stage: constitution
date: 2025-12-26
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Claude Code
command: sp.constitution
labels: [constitution, setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - null
---

## Prompt

```text

Project: AI/Spec-Driven Book Creation with Integrated RAG Chatbot

Overview:
Write and publish a technical book using Docusaurus and deploy it to GitHub Pages.
The book will be authored using Spec-Kit Plus and Claude Code.
An embedded Retrieval-Augmented Generation (RAG) chatbot will be developed to answer user questions based on the book's content.

Core principles:
- Specification-first development using Spec-Kit Plus
- High factual accuracy through verified technical documentation
- Clear explanations for software engineers and AI students
- Reproducibility of code, prompts, and system architecture
- Modular and maintainable AI-native system design

Key components:
- Book authoring with Docusaurus
- Spec-driven content generation using Claude Code
- Deployment via GitHub Pages
- Embedded RAG chatbot inside the published book
- Backend API built with FastAPI
- Vector search using Qdrant Cloud (Free Tier)
- Metadata and session storage using Neon Serverless Postgres
- AI orchestration using OpenAI Agents / ChatKit SDKs

Key standards:
- All technical claims must be verifiable from official documentation
- Architecture decisions must be justified and documented
- Code examples must be runnable and reproducible
- Prompts and specs must be explicitly defined
- RAG responses must cite retrieved context

RAG chatbot requirements:
- Answer questions based on the full book content
- Support answering questions based only on user-selected text
- Prevent hallucinations by restricting answers to retrieved context
- Clearly indicate when information is not found in the context
- Maintain low-latency responses suitable for web embedding

Documentation standards:
- Markdown-first content
- Code snippets with explanations
- Diagrams for system architecture and data flow
- Step-by-step setup guides

Constraints:
- Hosting: GitHub Pages (frontend), Cloud services free tiers only
- Backend: FastAPI
- Vector DB: Qdrant Cloud Free Tier
- Database: Neon Serverless Postgres
- AI SDKs: OpenAI Agents / ChatKit
- Book structure must be compatible with Docusaurus

Success criteria:
- Book successfully deployed on GitHub Pages
- RAG chatbot embedded and functional within the book
- Chatbot answers strictly based on book content or selected text
- All specs traceable to implementation
- Project reproducible by following documentation end-to-end
```

## Response snapshot

Created the initial constitution for the AI/Spec-Driven Book Creation with Integrated RAG Chatbot project, establishing core principles and governance structure. The constitution includes six key principles:

1. Specification-First Development
2. Factual Accuracy and Verifiability
3. RAG Integrity and Hallucination Prevention
4. Modular and Maintainable System Design
5. Performance and Latency Optimization
6. Reproducibility and Documentation Standards

Updated related templates to align with the new constitution:
- plan-template.md: Added constitution check items
- spec-template.md: Added functional requirements reflecting constitution principles
- tasks-template.md: Added foundational tasks related to constitution principles

## Outcome

- ✅ Impact: Created foundational governance document for the project
- 🧪 Tests: N/A
- 📁 Files: Updated constitution and related templates
- 🔁 Next prompts: Plan and implement initial features following the constitution
- 🧠 Reflection: Constitution provides clear guidelines for future development decisions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification following constitution principles