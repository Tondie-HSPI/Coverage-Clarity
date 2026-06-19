from fastapi import UploadFile

from app.schemas.analysis import AnalysisResponse, IntakeRequest, UploadDescriptor
from app.services.analysis_service import AnalysisService


class UploadAnalysisService:
    def __init__(self) -> None:
        self.analysis_service = AnalysisService()

    async def run_uploads(
        self,
        account_role: str,
        files: list[UploadFile],
        document_types: list[str] | None = None
    ) -> AnalysisResponse:
        documents: list[UploadDescriptor] = []

        for index, file in enumerate(files):
            content = await file.read()
            if document_types and index < len(document_types):
                document_type = document_types[index]
            else:
                document_type = self._infer_document_type(file.filename or "")
                if document_type == "supporting_doc" and len(files) > 1:
                    document_type = "contract" if index == 0 else "coi"
            documents.append(
                UploadDescriptor(
                    document_id=f"{index}-{file.filename}",
                    document_type=document_type,
                    file_name=file.filename,
                    content=content.decode("utf-8", errors="ignore"),
                    binary_payload=content
                )
            )

        payload = IntakeRequest(account_role=account_role, documents=documents)
        return self.analysis_service.run(payload)

    def _infer_document_type(self, file_name: str) -> str:
        lowered = file_name.lower()
        if "coi" in lowered or "certificate" in lowered:
            return "coi"
        if "policy" in lowered or "endorsement" in lowered:
            return "policy"
        if "contract" in lowered or "agreement" in lowered:
            return "contract"
        return "supporting_doc"
