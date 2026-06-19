from app.schemas.analysis import DecisionItem, EmailDraft


class CoiRequestService:
    def build_email_draft(self, items: list[DecisionItem]) -> EmailDraft | None:
        requested_items = [
            self._request_line(item)
            for item in items
            if item.state in {"missing", "unmet", "needs_review"}
        ]
        requested_items = [item for item in requested_items if item]

        if not requested_items:
            return None

        bullets = "\n".join(f"- {item}" for item in requested_items)
        body = (
            "Hello,\n\n"
            "Please review the insurance requirements below and provide a revised certificate "
            "of insurance and any applicable policy endorsements needed to support them:\n\n"
            f"{bullets}\n\n"
            "Please confirm whether each requested item is included by endorsement and provide "
            "copies of the applicable endorsement forms where available. Certificate wording "
            "alone may not be sufficient evidence of coverage.\n\n"
            "Please let us know if any requested item cannot be provided or requires additional "
            "information from the insured.\n\n"
            "Thank you,"
        )

        return EmailDraft(
            subject="Request for revised COI and supporting endorsements",
            body=body,
            requested_items=requested_items,
        )

    def _request_line(self, item: DecisionItem) -> str:
        requirement = item.requirement.strip()
        if item.state == "missing":
            return f"{item.obligation_type}: provide evidence meeting the contract requirement ({requirement})."
        if item.obligation_type == "Cyber Liability" and item.state == "unmet":
            return (
                "Cyber Liability / Tech E&O: provide evidence that the required limit and coverage components are included "
                f"({requirement}). Current evidence: {item.evidence_requirement or 'not confirmed'}."
            )
        if item.state == "unmet":
            evidence = item.evidence_requirement or "current evidence does not meet the requirement"
            return (
                f"{item.obligation_type}: correct or provide supporting evidence for "
                f"{requirement}. Current evidence: {evidence}."
            )
        return f"{item.obligation_type}: confirm and provide supporting documentation for {requirement}."
