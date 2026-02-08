---
name: frontend-page-builder
description: Build responsive frontend pages using reusable components, clean layouts, and modern styling techniques.
---

# Frontend Page & Component Development

## Instructions

1. *Page structure*
   - Semantic HTML5 layout
   - Clear section hierarchy
   - Reusable components

2. *Layout & styling*
   - Flexbox and Grid-based layouts
   - Consistent spacing and alignment
   - Scalable typography system

3. *Components*
   - Buttons, cards, forms, navbars
   - Component-based structure
   - State-ready styles (hover, active, focus)

4. *Responsiveness*
   - Mobile-first design
   - Breakpoints for tablet & desktop
   - Fluid layouts

## Best Practices
- Use semantic tags (header, main, section, footer)
- Keep components reusable and modular
- Follow consistent naming conventions (BEM or utility-based)
- Optimize for accessibility (contrast, focus states)
- Test on multiple screen sizes

## Example Structure
```html
<main class="page-container">
  <header class="site-header">
    <nav class="navbar">
      <h1 class="logo">Brand</h1>
      <ul class="nav-links">
        <li><a href="#">Home</a></li>
        <li><a href="#">About</a></li>
      </ul>
    </nav>
  </header>

  <section class="content-grid">
    <article class="card">
      <h2>Component Title</h2>
      <p>Reusable component content.</p>
      <button class="btn-primary">Action</button>
    </article>
  </section>
</main>