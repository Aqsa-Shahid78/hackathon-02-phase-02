---
name: auth-skill
description: Implement secure authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. *User Signup*
   - Validate input (email, password, confirmation)
   - Enforce strong password rules
   - Prevent duplicate accounts
   - Normalize and sanitize user data

2. *User Signin*
   - Authenticate using email/username and password
   - Compare hashed passwords securely
   - Return clear, non-revealing error messages
   - Protect against brute-force attempts

3. *Password Security*
   - Hash passwords using a strong algorithm (bcrypt, argon2, or scrypt)
   - Never store plaintext passwords
   - Use unique salts per user
   - Support password reset flows when applicable

4. *JWT Authentication*
   - Issue short-lived access tokens
   - Use refresh tokens when required
   - Sign tokens with secure secrets or key pairs
   - Validate and decode tokens on protected routes

5. *Better Auth Integration*
   - Configure Better Auth providers and secrets
   - Delegate token/session management where possible
   - Align Better Auth flows with existing auth logic
   - Handle callbacks, redirects, and session validation

## Best Practices
- Use HTTPS everywhere
- Keep auth logic isolated from business logic
- Never leak authentication failure details
- Rotate secrets and keys regularly
- Log auth events without sensitive data
- Follow least-privilege access rules

## Example Flow
```text
User Signup
→ Validate input
→ Hash password
→ Store user
→ Issue JWT / session

User Signin
→ Verify credentials
→ Generate token
→ Return authenticated response