---
id: 1
title: Update CLAUDE.md with Project Config
stage: general
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: none
branch: main
user: user
command: sp.resume
labels: ["claude-md", "project-setup", "agent-delegation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - CLAUDE.md
tests:
  - none
---

## Prompt

**Update the "claude.md" file based on my project requirements .
In this file :**
- Use Auth Agent for authentication
- Use API agent for API-related logic
-Use frontend Agent for frontend development (e.g., Next.js)
- Use DB Agent for database design and operations
-Use fast API backend Agent for backend development

Below are mt project requirements :

''' """ Phase II: Todo Full-Stack Web Application
Basic Level Functionality
Objective: Using Claude Code and Spec-Kit Plus transform the console app into a modern
multi-user web application with persistent storage.
Requirements
• Implement all 5 Basic Level features as a web application
• Create RESTful API endpoints
• Build responsive frontend interface
• Store data in Neon Serverless PostgreSQL database
• Authentication – Implement user signup/signin using Better Auth
Technology Stack
Layer Technology
Frontend Next.js 16+ (App Router)
Backend Python FastAPI
ORM SQLModel
Database Neon Serverless PostgreSQL
Spec-Driven Claude Code + Spec-Kit P

## Response snapshot

Updated CLAUDE.md with:
1. Project overview section (Todo Full-Stack Web App, Phase II objective, requirements)
2. Technology stack table (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth)
3. Agent Delegation Rules with 4 agents mapped to domains:
   - Auth Agent (auth-flow-handler) for authentication/Better Auth
   - FastAPI Backend Agent (fastapi-backend) for API/backend
   - Frontend Agent (nextjs-frontend-builder) for Next.js UI
   - DB Agent (neon-database-ops) for database/Neon
4. Agent Coordination Rules for cross-domain work
5. Target application code structure (frontend/ and backend/ directories)

## Outcome

- Impact: CLAUDE.md now provides clear project context and agent routing rules for all future development
- Tests: none (configuration file update)
- Files: CLAUDE.md modified
- Next prompts: /sp.constitution to define project principles, then /sp.specify for feature specs
- Reflection: Clean separation of agent responsibilities with coordination rules prevents overlap confusion

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): manual review PASS - all placeholders filled, agent mappings correct
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
