---
name: database-skill
description: Design relational database schemas, create tables, and manage migrations using best practices. Use for backend and data-driven applications.
---

# Database Schema & Migration Design

## Instructions

1. *Schema design*
   - Identify core entities and relationships
   - Normalize data where appropriate
   - Define primary and foreign keys
   - Choose correct data types

2. *Table creation*
   - Create tables with clear, consistent naming
   - Apply constraints (NOT NULL, UNIQUE, CHECK)
   - Use indexes for frequently queried fields
   - Define default values where applicable

3. *Migrations*
   - Use versioned, incremental migrations
   - Support forward and backward migrations
   - Avoid destructive changes without safeguards
   - Keep migrations small and focused

## Best Practices
- Prefer explicit schemas over implicit structures
- Use snake_case or consistent naming conventions
- Design for future changes, not just current needs
- Separate domain data from audit/metadata fields
- Document schema decisions and trade-offs

## Example Structure
```sql
CREATE TABLE todos (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  priority VARCHAR(10) CHECK (priority IN ('high', 'medium', 'low')),
  is_completed BOOLEAN DEFAULT FALSE,
  due_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);