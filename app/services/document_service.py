import logging
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption, WordFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

logger = logging.getLogger(__name__)
SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


class DocumentService:
    @staticmethod
    def validate_document_path(file_path: str) -> Path:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Document does not exist: {file_path}")
        if not path.is_file():
            raise ValueError(f"Document path is not a file: {file_path}")
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError("Only PDF and DOCX files are supported.")
        return path

    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        path = DocumentService.validate_document_path(file_path)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
                InputFormat.DOCX: WordFormatOption(),
            }
        )
        result = converter.convert(str(path))
        text = result.document.export_to_markdown()
        logger.info("Extracted %d chars from %s", len(text), path.name)
        return text
