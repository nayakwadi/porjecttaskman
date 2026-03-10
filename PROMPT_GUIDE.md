# AI Prompt Engineering Guide for Developers

> Best practices for writing effective prompts when working with AI coding assistants (e.g., Cursor)

---

## 10 Key Principles

1. **Ask the right questions** to get the right response.

2. **Be very specific** – Define requirements, functionalities, output formats, and precise scenarios.

3. **Break down the application** into modules with specific instructions (libraries, methods, approaches).

4. **Provide context**:
   - Who you are
   - What you're trying to do
   - Desired output format
   - Reference files
   - Expected outcomes with examples

5. **Precision yields better output** – The more precise the prompt, the better the first attempt. Iterate as you make changes.

6. **Understand tokenization** – Prompts are converted to tokens; LLMs process tokens to generate output.

7. **Structure your prompts** – Split into sections and be specific in each section.

8. **Iterate and refine** – Continuously improve your prompts.

9. **Use transcripts** – Generated transcripts can become your main `prompts.md` file; keep modifying for better outcomes.

10. **Explore different modes**:
    - **Ask** – e.g., To understand a code block in a specific file
    - **Plan** – e.g., Create a step-by-step plan to build application X with requirements ABC and target users expecting XYZ functionalities
    - **Agent** – e.g., Generate code based on prompts with or without context/examples

---

## Examples

### Worst Prompt

```
Build a task management application using basic Flask, python, html, SQLite
```

**Problem:** This prompt is too broad. It allows the AI excessive creativity and rarely produces a working application. You may end up rewriting prompts until you see valid results.

### Better Prompt

Construct a detailed prompt with distinct pieces – each with specific instructions, examples, and suggestions. Include:

- Context
- Objective
- Functionalities
- Requirements
- Application Setup
- etc.

Refer to `cursor_prompts_taskmanager_app.md` for reference.

### Shot Strategies

> **Avoid Zero Shot prompts** (no examples). Always use **One Shot** or **Multi Shot** examples.

#### One Shot Example

> Write a regular expression that matches valid email addresses. Test it with:
>
> - `valid@example.com`
> - `invalid@`
> - `myusername.com`
> - `@nodomain.com`

#### Few Shot / Multi Shot Example

> Create a Day-to-day Task Planner application that runs locally. It should have capabilities similar to:
>
> - Example 1: Outlook task management
> - Example 2: iPhone Reminders
> - Example 3: Google Calendar

### Chain-of-Thought

Provide hints for a step-by-step reasoning approach in your prompts.

**Example:** Design a database schema for a task management application. Think through each entity, relationships, and constraints step by step.

> For larger projects, include necessary project folders/files and reference them in the context.

### Multiple Outputs

Request multiple outputs and select the best one.

**Example:** Write a regular expression that validates email addresses. Create 4 examples, evaluate pros and cons of each, and pick the best method for maximum efficiency at scale.

---

## Cursor IDE Rules

| Setting | Recommendation |
|--------|-----------------|
| **Level** | Define standard rules at user level or **project level** |
| **Team setup** | Use **project-level** rules so every developer follows org-wide and project-wide standards |

---

## Quick Reference

| Principle | Action |
|-----------|--------|
| Specificity | Define requirements, formats, scenarios precisely |
| Structure | Split prompts into sections |
| Examples | Use One Shot or Multi Shot (avoid Zero Shot) |
| Context | Who, what, format, reference files |
| Iteration | Refine prompts continuously |
| Modes | Ask, Plan, Agent – choose appropriately |
