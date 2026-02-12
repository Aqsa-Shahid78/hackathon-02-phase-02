---
id: 2
title: Create Project Constitution
stage: constitution
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "principles", "project-setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution

Project: Todo Full-Stack Web Application

Core principles:
- User-centered design with intuitive interface
- Security through JWT-based authentication
- Scalability by leveraging Neon Serverless PostgreSQL
- Responsiveness with mobile-first design approach
- High performance with efficient backend API and optimized queries

Key standards:
- All tasks and user data must be securely handled and isolated
- Code quality and structure must follow best practices for scalability
- Authentication and authorization must be secure with JWT tokens
- RESTful API endpoints should follow industry standards
- User experience should be seamless across different devices (desktop and mobile)

Constraints:
- Frontend built with Next.js 16+ using App Router
- Backend developed with FastAPI and SQLModel ORM
- Authentication with Better Auth integrated for JWT token issuance
- Database: Neon Serverless PostgreSQL
- API endpoints must include:
  - GET /api/{user_id}/tasks
  - POST /api/{user_id}/tasks
  - GET /api

## Response snapshot

Created constitution v1.0.0 with 5 core principles:
1. **I. User-Centered Design** — Intuitive UX, inline validation, WCAG 2.1 AA, minimal clicks
2. **II. Security-First** — Better Auth + JWT, bcrypt/argon2id, data isolation, rate limiting, no secret hardcoding
3. **III. Scalability** — Neon connection pooling, UUID PKs, timestamps, pagination, reversible migrations
4. **IV. Mobile-First Responsiveness** — 320px-first design, 44px touch targets, Tailwind mobile-first ordering
5. **V. High Performance** — <200ms p95 single resource, async FastAPI, Server Components default, loading states

Added Technology Stack & Constraints section with mandatory stack table and RESTful API contract definitions.
Added Development Workflow & Quality Gates with code quality standards, testing requirements, and agent delegation rules.
Added Governance with compliance, amendment, versioning, conflict resolution, and complexity justification policies.

Sync Impact Report: All 3 templates (plan, spec, tasks) verified compatible. No follow-up TODOs.

## Outcome

- Impact: Project constitution ratified at v1.0.0 — all development decisions now governed by 5 declarative, testable principles
- Tests: none (governance document)
- Files: .specify/memory/constitution.md created (184 lines)
- Next prompts: /sp.specify to create feature specification for the todo app
- Reflection: All user-provided principles mapped cleanly to testable MUST-level rules. API contracts included per user constraints. Conflict resolution order established (Security > UX > others).

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): manual validation PASS — no unresolved placeholders, all dates ISO, all principles declarative with MUST language
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
