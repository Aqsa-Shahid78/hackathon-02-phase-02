---
name: backend-core
description: Generate backend routes, handle HTTP requests/responses, and connect applications to databases.
---

# Backend Routes & Database Handling

## Instructions

1. *Routing setup*
   - Define RESTful routes
   - Use proper HTTP methods (GET, POST, PUT, DELETE)
   - Organize routes by feature or module

2. *Request & response handling*
   - Parse request parameters and body
   - Validate incoming data
   - Send structured JSON responses
   - Handle errors with proper status codes

3. *Database integration*
   - Connect to database (SQL or NoSQL)
   - Perform CRUD operations
   - Use models or schemas
   - Handle async database queries safely

## Best Practices
- Follow REST API conventions
- Use environment variables for DB credentials
- Validate and sanitize user input
- Implement proper error handling and logging
- Keep business logic separate from routes

## Example Structure
```js
// routes/userRoutes.js
import express from "express";
import User from "../models/User.js";

const router = express.Router();

router.post("/users", async (req, res) => {
  try {
    const user = await User.create(req.body);
    res.status(201).json(user);
  } catch (error) {
    res.status(500).json({ message: "Server error" });
  }
});

router.get("/users", async (req, res) => {
  const users = await User.find();
  res.json(users);
});

export default router;