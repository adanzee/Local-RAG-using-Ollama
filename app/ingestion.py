# Handles document loading + OCR
import os
import sys

lib_path = r"path_to_your_project"
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
    sys.path.insert(0, os.getcwd())

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.document_converter import WordFormatOption


def extract_text_from_file(file_path: str) -> str:
    # Enable OCR
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
            InputFormat.DOCX: WordFormatOption(),
        }
    )

    result = converter.convert(file_path)
    return result.document.export_to_markdown()
