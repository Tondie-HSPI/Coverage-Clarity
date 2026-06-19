import re

from app.rules.loader import load_endorsement_rules


class EndorsementParser:
    def __init__(self) -> None:
        self.rules = load_endorsement_rules()

    def parse(self, obligation_type: str, text: str) -> list[str]:
        normalized_type = obligation_type.lower()
        if "additional insured" in normalized_type:
            section_rules = self.rules["additional_insured"]
        elif "waiver of subrogation" in normalized_type:
            section_rules = self.rules["waiver_of_subrogation"]
        else:
            section_rules = {}

        tokens: list[str] = []
        for form_rule in section_rules.get("form_patterns", []):
            if re.search(form_rule["regex"], text, re.IGNORECASE):
                self._add_unique(tokens, form_rule["form_number"])
                for meaning in form_rule.get("meaning", []):
                    self._add_unique(tokens, meaning)

        for label, pattern in section_rules.get("phrase_patterns", {}).items():
            if re.search(pattern, text, re.IGNORECASE):
                self._add_unique(tokens, label)

        return tokens

    def compare(self, obligation_type: str, required_text: str, evidence_text: str) -> bool:
        required_tokens = self.parse(obligation_type, required_text)
        evidence_tokens = self.parse(obligation_type, evidence_text)

        if not required_tokens:
            return True

        evidence_set = {token.lower() for token in evidence_tokens}
        for token in required_tokens:
            if token.lower() not in evidence_set:
                return False
        return True

    def _add_unique(self, tokens: list[str], value: str) -> None:
        if value not in tokens:
            tokens.append(value)
