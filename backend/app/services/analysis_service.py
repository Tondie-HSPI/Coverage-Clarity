from uuid import uuid4

from app.comparison_layer.comparator import ComparisonLayer
from app.decision_support.advisor import DecisionSupportLayer
from app.extraction_layer.parser import ExtractionLayer
from app.governance.constraints import GovernanceLayer
from app.input_layer.intake import IntakeLayer
from app.obligation_modeling.modeler import ObligationModeler
from app.schemas.analysis import AnalysisResponse, IntakeRequest
from app.services.coi_request_service import CoiRequestService
from app.state_engine.engine import StateEngine
from app.validation_layer.validator import ValidationLayer


class AnalysisService:
    def __init__(self) -> None:
        self.intake = IntakeLayer()
        self.extraction = ExtractionLayer()
        self.modeler = ObligationModeler()
        self.validation = ValidationLayer()
        self.state_engine = StateEngine()
        self.comparison = ComparisonLayer()
        self.decision_support = DecisionSupportLayer()
        self.governance = GovernanceLayer()
        self.coi_requests = CoiRequestService()

    def run(self, payload: IntakeRequest) -> AnalysisResponse:
        state = self.intake.create_state(payload)
        state = self.governance.apply(state)
        analysis_mode = self._determine_analysis_mode(payload)

        parsed_documents = self.extraction.parse(payload.documents)
        obligations = self.modeler.build(parsed_documents)
        validations = self.validation.validate(obligations)
        if analysis_mode == "comparison":
            decision_items = self.comparison.compare(obligations)
        else:
            decision_items = self.state_engine.assign(obligations, validations)
        decision_items = self.decision_support.refine(decision_items)
        decision_items = self.governance.validate_outputs(decision_items)
        email_draft = self.coi_requests.build_email_draft(decision_items)

        overall_confidence = round(
            sum(obligation.confidence for obligation in obligations) / len(obligations), 2
        ) if obligations else 0.0

        return AnalysisResponse(
            workflow_id=str(uuid4()),
            overall_confidence=overall_confidence,
            analysis_mode=analysis_mode,
            items=decision_items,
            parsed_documents=parsed_documents,
            validations=validations,
            email_draft=email_draft,
        )

    def _determine_analysis_mode(self, payload: IntakeRequest) -> str:
        document_types = {document.document_type for document in payload.documents}
        has_contract = "contract" in document_types
        has_evidence_docs = bool(document_types.intersection({"coi", "policy", "supporting_doc"}))

        if has_contract and has_evidence_docs:
            return "comparison"
        if has_contract:
            return "contract_requirements"
        return "document_presence"
