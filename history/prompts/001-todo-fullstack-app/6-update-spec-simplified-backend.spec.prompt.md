---
id: 6
title: Update Spec with Simplified Backend Structure
stage: spec
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 001-todo-fullstack-app
branch: 001-todo-fullstack-app
user: user
command: /sp.specify
labels: ["spec", "backend", "structure", "simplification", "flat-layout"]
links:
  spec: specs/001-todo-fullstack-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-fullstack-app/spec.md
  - specs/001-todo-fullstack-app/plan.md
  - specs/001-todo-fullstack-app/tasks.md
tests:
  - none
---

## Prompt

/sp.specify Todo Full-Stack Web Application

(Re-run with updated input specifying a simplified backend folder structure)

User provided a Backend Folder Structure section:
- app/main.py - FastAPI application entry point
- app/config.py - Application settings
- app/models.py - SQLModel database models (single file, not split)
- app/routes/tasks.py - Task CRUD endpoints
- app/schemas.py - Pydantic models for request validation

## Response snapshot

Updated 3 SDD artifacts to reflect the user's simplified flat backend structure:

**spec.md**: Added "Backend Folder Structure" section at the end documenting the flat layout with rationale. Structure uses single files (models.py, schemas.py, security.py, exceptions.py) and routes/ directory instead of nested packages.

**plan.md**: Replaced the Source Code backend tree from multi-directory (models/, schemas/, services/, core/, api/v1/endpoints/) to flat layout. Updated Phase 3 and Phase 4 descriptions with correct file paths.

**tasks.md**: Updated 25+ tasks across all 9 phases with corrected file paths:
- models/user.py + models/task.py → models.py
- schemas/auth.py + schemas/task.py → schemas.py
- api/v1/endpoints/auth.py → routes/auth.py
- api/v1/endpoints/tasks.py → routes/tasks.py
- services/auth_service.py → routes/auth.py (inline)
- services/task_service.py → routes/tasks.py (inline)
- core/security.py → security.py
- core/exceptions.py → exceptions.py
- core/middleware.py → main.py (inline)
- api/v1/router.py → routes/__init__.py

Verified zero stale old-path references remain in quickstart.md, contracts/api.md, or research.md.

## Outcome

- Impact: All SDD artifacts now consistent with simplified flat backend structure
- Tests: none (spec/plan/tasks update)
- Files: spec.md, plan.md, tasks.md updated (3 files)
- Next prompts: /sp.implement to begin executing tasks with the corrected file paths
- Reflection: The flat structure is a good fit for this project scope (2 models, ~8 endpoints). Eliminates 7+ __init__.py files and makes navigation simpler. Task count remains 68 but file paths are corrected throughout.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Path consistency check PASS — grep for old paths returns zero matches across all spec artifacts
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
