# Lovable Frontend API Contract

Use Coverage Clarity as a standalone COI review API. The Lovable app should call the
API, render the findings, and let the user edit the generated email before
sending it from their own email system.

## Base URL

Local:

```text
http://127.0.0.1:8013
```

Production:

```text
https://your-api-domain.example
```

## Health Check

```http
GET /health
```

Expected response:

```json
{"status":"ok"}
```

## Paste/Text Review

```http
POST /api/coi-review
Content-Type: application/json
```

Example body:

```json
{
  "account_role": "reviewer",
  "documents": [
    {
      "document_id": "contract-1",
      "document_type": "contract",
      "file_name": "contract.txt",
      "content": "Commercial General Liability insurance with limits of $1,000,000 each occurrence and $2,000,000 aggregate. The owner and contractor must be additional insureds by endorsement. Waiver of subrogation is required."
    },
    {
      "document_id": "coi-1",
      "document_type": "coi",
      "file_name": "coi.txt",
      "content": "Certificate of liability insurance. General liability limits are $500,000 each occurrence and $1,000,000 aggregate."
    }
  ]
}
```

## PDF/Text Upload Review

```http
POST /api/coi-review-upload
Content-Type: multipart/form-data
```

Fields:

- `account_role`: `reviewer`
- `files`: one or more `.pdf`, `.txt`, or `.md` files
- `document_types`: optional repeated field matching file order, such as
  `contract`, `coi`, `policy`, or `supporting_doc`

If `document_types` is omitted and multiple files are uploaded, the backend
treats the first file as the contract and later files as COI evidence.

## Response Shape

Important fields:

```json
{
  "workflow_id": "uuid",
  "overall_confidence": 0.67,
  "analysis_mode": "comparison",
  "items": [
    {
      "obligation_type": "General Liability",
      "requirement": "$1,000,000 / $2,000,000",
      "evidence_requirement": "$500,000 / $1,000,000",
      "state": "unmet",
      "explanation": "Contract requires one thing, but evidence shows another.",
      "next_action": "Escalate to reviewer and request corrected supporting evidence."
    }
  ],
  "email_draft": {
    "subject": "Request for revised COI and supporting endorsements",
    "body": "Hello...",
    "requested_items": [
      "General Liability: correct or provide supporting evidence..."
    ],
    "requires_human_review": true
  }
}
```

## Frontend Screens

Suggested Lovable flow:

1. Upload or paste contract requirements.
2. Upload or paste current COI / policy / endorsement evidence.
3. Show supported, unmet, and missing requirements.
4. Include management liability findings when present, such as D&O, EPLI,
   Fiduciary, Crime/Fidelity, and Cyber Liability.
5. Let the user choose recipient type: insured's broker, insurance agent, or
   carrier representative.
6. Show editable subject/body and require review before opening email.

## Safety Copy

Use this notice in the UI:

```text
This tool provides decision support only. It does not certify coverage,
confirm compliance, bind insurance, or provide legal or insurance advice.
All outputs require human review.
```
