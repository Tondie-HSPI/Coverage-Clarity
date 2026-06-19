from app.schemas.analysis import DecisionItem


class DecisionSupportLayer:
    def refine(self, items: list[DecisionItem]) -> list[DecisionItem]:
        refined: list[DecisionItem] = []
        for item in items:
            explanation = item.explanation
            next_action = item.next_action
            if item.state == "met":
                explanation = "Evidence supports this obligation."
                next_action = "No immediate action needed."
            refined.append(
                item.model_copy(update={"explanation": explanation, "next_action": next_action})
            )
        return refined

