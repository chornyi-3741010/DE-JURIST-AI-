"""Document manager: detection, extraction, metadata"""
from pathlib import Path
import mimetypes
from typing import Tuple, List, Dict, Any
from .logger import logger


def detect_type(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() in ('.pdf',):
        return 'pdf'
    if p.suffix.lower() in ('.docx', '.doc'):
        return 'docx'
    if p.suffix.lower() in ('.txt', '.md'):
        return 'text'
    if p.suffix.lower() in ('.png', '.jpg', '.jpeg'):
        return 'image'
    return mimetypes.guess_type(p.name)[0] or 'binary'


def extract_text(path: str) -> Tuple[str, List[str], Dict[str,Any]]:
    p = Path(path)
    warnings: List[str] = []
    text = ''
    meta: Dict[str,Any] = {'size': p.stat().st_size, 'name': p.name}
    try:
        if p.suffix.lower() == '.pdf':
            try:
                import PyPDF2
                with p.open('rb') as fh:
                    reader = PyPDF2.PdfReader(fh)
                    text = '\n'.join([pg.extract_text() or '' for pg in reader.pages])
                if not text.strip():
                    warnings.append('PDF likely scanned, no extractable text')
            except Exception as e:
                warnings.append('PyPDF2 error: '+str(e))
        elif p.suffix.lower() in ('.docx',):
            try:
                import docx
                doc = docx.Document(p)
                text = '\n'.join([para.text for para in doc.paragraphs])
            except Exception as e:
                warnings.append('python-docx error: '+str(e))
        elif p.suffix.lower() in ('.png','.jpg','.jpeg'):
            try:
                from PIL import Image
                import pytesseract
                img = Image.open(p)
                text = pytesseract.image_to_string(img, lang='deu+rus+ukr')
            except Exception as e:
                warnings.append('OCR error: '+str(e))
        else:
            try:
                text = p.read_text(encoding='utf-8')
            except Exception as e:
                warnings.append('Text read error: '+str(e))
    except Exception as e:
        warnings.append('General extract error: '+str(e))
    logger.debug('extract_text %s -> %d chars, warnings=%s', p.name, len(text), warnings)
    return text, warnings, meta
