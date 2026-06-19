from app.extraction_layer.insurance_parser import InsuranceDocumentParser
from app.schemas.analysis import ParsedDocument, UploadDescriptor


class ExtractionLayer:
    def __init__(self) -> None:
        self.parser = InsuranceDocumentParser()

    def parse(self, documents: list[UploadDescriptor]) -> list[ParsedDocument]:
        return self.parser.parse(documents)
