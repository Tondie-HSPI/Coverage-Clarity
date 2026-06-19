from app.schemas.analysis import Obligation, ValidationResult


class ValidationLayer:
    def validate(self, obligations: list[Obligation]) -> list[ValidationResult]:
        results: list[ValidationResult] = []
        for obligation in obligations:
            results.append(
                ValidationResult(
                    obligation_type=obligation.obligation_type,
                    matched_evidence=[obligation.source] if obligation.raw_status != "missing" else [],
                    missing_fields=["requirement"] if obligation.raw_status == "missing" else [],
                    comparison_notes=[
                        "Parsed from extracted insurance sections"
                        if obligation.raw_status != "missing"
                        else "No structured pattern match found"
                    ]
                )
            )
        return results
