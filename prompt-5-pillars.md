# 5 Pillar Prompt Template

> This framework addresses a specific gap in how most developers interact with AI tools. Together, the five pillars transform vague requests into comprehensive specifications that produce production-grade code on the first try.

---

## Overview: The Five Pillars

| Pillar | What It Solves |
|--------|----------------|
| **Context** | Environment & constraints – Prevents assumptions about scale, deployment, and integration |
| **Stakeholders** | Who this serves – Ensures code works for developers, ops, security, and end users |
| **Standards** | Rules of engagement – Creates consistent patterns across your entire codebase |
| **Outcomes** | Clear success criteria – Eliminates vague results with measurable definitions of "done" |
| **Edge Cases** | What could go wrong – Handles failures, errors, and unexpected scenarios |

---

## Template

Use this structure when crafting AI prompts:

```
I need to [WHAT YOU WANT TO BUILD]

Context:
- Environment: [Where will this run?]
- Scale: [How many users/requests?]
- Constraints: [What limitations exist?]

End Users:
- [WHO will use it and HOW]
- [WHO will maintain it]
- [WHO needs visibility into it]

Follow these standards:
- Architecture: [Pattern to follow]
- Code style: [Standards to apply]
- Testing: [Coverage and approach]

Success means:
- [Specific performance requirement]
- [Key feature requirement]
- [Operational requirement]

Handle these edge cases:
- [Most likely failure]
- [Security concern]
- [Resource constraint]
```

---

## Quick Reference Checklist

Use this checklist before every AI prompt to ensure you're applying all five pillars:

| # | Pillar | Question to Ask |
|---|--------|-----------------|
| 1 | Context | Have I described **WHERE** this runs and at **WHAT SCALE**? |
| 2 | Stakeholders | Have I considered **ALL** people who will interact with this? |
| 3 | Standards | Have I specified the **PATTERNS** and **PRACTICES** to follow? |
| 4 | Outcomes | Can I clearly define what **DONE** looks like? |
| 5 | Edge Cases | What could **GO WRONG** and how should it be handled? |

---

## Examples

### Bad Prompt (Without 5 Pillar Framework)

> Create a notification service that sends push notifications to mobile users. It should be scalable and handle a lot of traffic. Make sure it's reliable and integrates with our existing systems.

**Problems:** Vague scale, no stakeholders, no standards, no measurable outcomes, no edge cases.

---

### Good Prompt (With 5 Pillar Template)

> Create a notification service that:
>
> **[CONTEXT]** Runs in our Kubernetes cluster alongside 20 other microservices, processes 1M+ notifications daily, integrates with existing RabbitMQ message bus
>
> **[STAKEHOLDERS]** Serves mobile app users expecting real-time updates; maintained by a 5-person backend team; monitored by SRE team needing detailed metrics
>
> **[STANDARDS]** Follow our hexagonal architecture pattern, use structured logging with correlation IDs, include OpenAPI specs, minimum 80% test coverage
>
> **[OUTCOMES]** Process notifications within 500ms p99, support 10K concurrent WebSocket connections, enable/disable notifications per user per type, provide delivery status tracking
>
> **[EDGE CASES]** Handle message bus failures with local queuing, manage WebSocket reconnection gracefully, rate limit per user (100/hour), cope with malformed messages without crashing, scale horizontally during traffic spikes

---

## Key Insight: Why Structure Beats Iteration

| Approach | Result |
|----------|--------|
| Basic prompts | Plateau at low quality no matter how many times you iterate |
| 5-Pillar framework | Creates a consistent upward trajectory toward production-ready code |

> The difference isn't more words—it's **systematic structure** that compounds for exponentially better results.
