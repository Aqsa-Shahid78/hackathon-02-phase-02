---
id: 4
title: "Add OpenAPI response descriptions"
stage: green
date: "2026-02-09"
surface: agent
model: claude-opus-4-6
feature: 001-todo-fullstack-app
branch: main
user: classic-pc
command: implement
labels: ["openapi", "documentation", "api", "responses"]
links:
  spec: "specs/001-todo-fullstack-app/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/routes/auth.py
  - backend/app/routes/tasks.py
tests: []
---

## Prompt

have you created 201: {"description": "User created successfully"}, 400, 409, 200, 401, 422 response descriptions on endpoints?

## Response

Added explicit OpenAPI `responses` dictionaries to all route decorators:

**Auth routes:**
- POST /signup: 201, 400, 409, 422, 429
- POST /signin: 200, 401, 422, 429
- POST /signout: 204, 401

**Task routes:**
- POST create: 201, 401, 403, 422
- GET list: 200, 401, 403
- GET single: 200, 401, 403, 404
- PUT update: 200, 401, 403, 404, 422
- DELETE: 204, 401, 403, 404
- PATCH toggle: 200, 401, 403, 404

All descriptions now visible in auto-generated Swagger docs at /docs.

## Outcome

All 9 API endpoints now have complete OpenAPI response documentation with appropriate HTTP status codes and descriptions.
