from app.schemas.analysis import IntakeRequest


class IntakeLayer:
    def create_state(self, payload: IntakeRequest) -> dict:
        return {
            "role": payload.account_role,
            "documents": payload.documents,
            "parsed_documents": [],
            "obligations": [],
            "validations": [],
            "decision_items": []
        }

