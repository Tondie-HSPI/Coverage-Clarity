from app.schemas.analysis import DecisionItem, Obligation, ValidationResult


class StateEngine:
    def assign(self, obligations: list[Obligation], validations: list[ValidationResult]) -> list[DecisionItem]:
        validation_map = {item.obligation_type: item for item in validations}
        decision_items: list[DecisionItem] = []

        for obligation in obligations:
            validation = validation_map.get(obligation.obligation_type)
            state = "needs_review"
            if obligation.raw_status == "missing":
                state = "missing"
            elif obligation.raw_status == "unclear":
                state = "needs_review"
            elif validation and validation.matched_evidence and not validation.missing_fields:
                state = "met"

            decision_items.append(
                DecisionItem(
                    obligation_type=obligation.obligation_type,
                    requirement=obligation.requirement,
                    evidence_requirement=None,
                    state=state,
                    search_terms=obligation.search_terms,
                    source=obligation.source,
                    evidence_source=None,
                    source_excerpt=obligation.source_excerpt,
                    explanation="Obligation converted into a validated decision state.",
                    next_action="Review supporting citation and confirm evidence."
                )
            )

        return decision_items
