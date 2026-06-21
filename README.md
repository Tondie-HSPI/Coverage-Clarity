# Coverage Clarity

**A decision-support prototype for commercial insurance intake and review.**

## Overview

Coverage Clarity explores how AI-assisted workflows can reduce friction in commercial insurance intake by helping users organize business context, map responses to carrier-facing questions, identify uncertainty, and preserve review checkpoints.

The application supports commercial insurance professionals working through contracts, Certificates of Insurance (COIs), policies, and endorsement evidence. It turns insurance requirements into structured review items, compares those requirements against uploaded evidence, and drafts a human-review email request for the insured's broker, insurance agent, or carrier representative.

The goal is not to replace professional judgment. The goal is to make fragmented, review-heavy information easier to inspect, document, and hand off.

## Operational Pain Point

Commercial insurance intake is often context-dependent and review-heavy:

- Business information may arrive through contracts, COIs, policies, emails, notes, or endorsement evidence.
- Business descriptions do not always map cleanly to carrier-facing questions or coverage requirements.
- Review quality depends on context, judgment, source evidence, and careful interpretation.
- Poorly structured intake can create rework, delays, unclear assumptions, and inconsistent documentation.
- Certificate wording, additional insured requirements, waivers of subrogation, and coverage limits often require human review before action.

Coverage Clarity is designed around that operational reality: the work is not simply "extract text." The work is organizing uncertainty so a reviewer can make a clearer decision.

## Decision-Support Approach

Coverage Clarity addresses the pain point by turning scattered insurance information into structured, reviewable outputs:

- Captures business and document context in a structured way.
- Extracts obligations and requirements from contracts, COIs, policies, and endorsements.
- Maps intake information to relevant insurance review questions.
- Compares requirements against uploaded evidence.
- Flags uncertain, incomplete, or unsupported information.
- Makes assumptions and confidence visible.
- Supports more consistent documentation and clearer handoffs.
- Produces a broker/agent/carrier follow-up draft for human review.

## Human-in-the-Loop Design

Coverage Clarity does not silently autofill forms, certify compliance, confirm coverage, bind insurance, or replace an insurance professional.

The goal is not to automate judgment away. The goal is to reduce cognitive load, surface uncertainty, and give reviewers a clearer packet of information to evaluate.

Human review is expected when requirements are ambiguous, evidence is incomplete, endorsement wording needs interpretation, or an output may affect a carrier-facing or insured-facing action.

## Governance and Auditability

The project is designed to preserve trust and reviewability through:

- Confidence indicators for extracted or compared items.
- Source/context visibility for review decisions.
- Review checkpoints before relying on generated outputs.
- Assumption tracking when evidence is incomplete or unclear.
- Clear separation between generated suggestions and final human-reviewed outputs.
- Refusal and boundary logic for unsupported or high-risk interpretations.

## Background

This started as a vision from my Applied AI & Business Analytics program: insurance and compliance teams spend too much time manually decoding contracts, COIs, and policies to figure out what's actually required and what's missing. I spent months exploring the problem, taking notes at conferences, and learning the tools, before building Compliance Explained as a first working prototype. Coverage Clarity is where that thinking landed: a more complete extraction, comparison, and decision-support workflow built end to end.

## Skills Demonstrated

- Operational workflow analysis.
- AI-assisted decision support.
- Commercial insurance process understanding.
- Human-in-the-loop system design.
- Structured intake and data mapping.
- Review queue and escalation logic.
- Governance-aware AI implementation.
- Full-stack prototype development.
- Documentation for regulated or high-friction workflows.

## Product Shape

- Frontend: Lovable or the existing Next.js app shell in this repo.
- Backend: FastAPI COI review API in `backend/app`.
- Deployment target: AWS through LeapStacks2 or another container-friendly path.

## Core Workflow

`Contract + COI / policy / endorsements -> Extract -> Compare -> Review -> Email draft`

## Current Checks

- General Liability limits.
- Umbrella / Excess limits.
- Additional Insured parties and endorsement signals.
- Waiver of Subrogation parties and endorsement signals.
- Certificate Holder and additional coverage notes.
- Management liability lines, including D&O, EPLI, Fiduciary, Crime/Fidelity, and Cyber Liability.
- Cyber / Tech E&O component checks, including privacy, network security, breach response, PCI/payment card, media liability, ransomware/extortion, dependent business interruption, computer fraud, social engineering, and regulatory defense signals.

## Architecture (RECKON-Aligned)

Coverage Clarity's backend follows the RECKON framework I use across my AI orchestration projects:

- **R - Request**: `input_layer/intake.py` builds initial state from the incoming request.
- **E - Extraction**: `extraction_layer/insurance_parser.py` parses contracts, COIs, and policies.
- **C - Context**: `obligation_modeling/modeler.py` builds structured obligations from extracted content.
- **K - Knowledge**: `governance/constraints.py` and `rules/*.yaml` apply domain rules and refusal logic.
- **O - Orchestration**: `state_engine/engine.py` assigns state across the review pipeline.
- **N - Next Best Action**: `decision_support/advisor.py` generates explanations and recommended next steps per item.

## Backend API

Run locally:

```powershell
.\start-backend.ps1
```

Default local API:

```text
http://127.0.0.1:8010
```

Health check:

```text
GET /health
```

Endpoints:

- `POST /api/coi-review` accepts pasted/structured text documents.
- `POST /api/coi-review-upload` accepts PDF, text, and Markdown uploads.
- Legacy aliases are also available: `POST /api/analyze` and `POST /api/analyze-upload`.

## Frontend

The existing Next.js app can remain as a project shell, but the production frontend may be built in Lovable. Use the API contract in:

```text
docs/LOVABLE_FRONTEND_API.md
```

## Deployment

- Dockerfile: `backend/Dockerfile`.
- Container port: `8080`.
- AWS / LeapStacks notes: `docs/AWS_LEAPSTACKS_LAUNCH.md`.
- Lovable frontend contract: `docs/LOVABLE_FRONTEND_API.md`.

## Suggested Portfolio Framing

This project is part of a broader portfolio focused on decision-support systems for operational teams working inside complex, regulated, or high-friction workflows.

## Future Improvements

- **Pay-ready flag**: a single top-level `pay_ready: true/false` field summarizing whether all required obligations are satisfied, alongside the detailed review-item list, so a CSR or business owner can get a yes/no answer before reviewing details.
- **Starter checklist mode**: let a user pick a business type (e.g. food truck, landscaper, photographer) and get a plain-English starter checklist of typical licenses, contracts, and insurance needs, for users who don't have a contract or COI to upload yet.

## Boundary

Coverage Clarity is decision support only. It does not certify compliance, confirm coverage, bind insurance, or provide legal or insurance advice. All outputs require human review.
