# Coverage Clarity API

Coverage Clarity is a standalone backend for COI review.

It compares contract insurance requirements against certificates of insurance,
policies, and endorsement evidence. It returns supported, unmet, and missing
items, plus a human-review email draft for the insured's broker, insurance
agent, or carrier representative.

The production frontend can be built in Lovable and connected through the API
contract in `docs/LOVABLE_FRONTEND_API.md`.

## Core Workflow

`Contract + COI / policy / endorsements -> Extract -> Compare -> Review -> Email draft`

## Current Checks

- General Liability limits
- Umbrella / Excess limits
- Additional Insured parties and endorsement signals
- Waiver of Subrogation parties and endorsement signals
- Certificate Holder and additional coverage notes
- Management liability lines, including D&O, EPLI, Fiduciary, Crime/Fidelity,
  and Cyber Liability
- Cyber / Tech E&O component checks, including privacy, network security, breach
  response, PCI/payment card, media liability, ransomware/extortion, dependent
  business interruption, computer fraud, social engineering, and regulatory
  defense signals
- Contract requirements versus COI/policy evidence

## Run Locally

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

## API

- `POST /api/coi-review` accepts pasted/structured text documents.
- `POST /api/coi-review-upload` accepts PDF, text, and Markdown uploads.
- Legacy aliases are also available: `POST /api/analyze` and
  `POST /api/analyze-upload`.

## Deployment

- Dockerfile: `backend/Dockerfile`
- Container port: `8080`
- AWS / LeapStacks notes: `docs/AWS_LEAPSTACKS_LAUNCH.md`
- Lovable frontend contract: `docs/LOVABLE_FRONTEND_API.md`

## Boundary

Coverage Clarity is decision support only. It does not certify compliance,
confirm coverage, bind insurance, or provide legal or insurance advice. All
outputs require human review.
