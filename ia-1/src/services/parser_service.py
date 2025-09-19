"""
Serviço de parsing de documentos
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import asyncio
from typing import Dict, Any, Optional
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ParserService:
    """Serviço para parsing de documentos"""
    
    def __init__(self):
        self.supported_formats = settings.SUPPORTED_FORMATS
        self.pymupdf_timeout = settings.PYMUPDF_TIMEOUT
        self.tesseract_timeout = settings.TESSERACT_TIMEOUT
        self.ocr_language = settings.OCR_LANGUAGE
    
    async def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Parse de documento principal"""
        try:
            file_extension = file_path.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                return await self._parse_pdf(file_path)
            elif file_extension in ['png', 'jpg', 'jpeg']:
                return await self._parse_image(file_path)
            elif file_extension == 'txt':
                return await self._parse_text(file_path)
            elif file_extension == 'docx':
                return await self._parse_docx(file_path)
            else:
                raise ValueError(f"Formato não suportado: {file_extension}")
                
        except Exception as e:
            logger.error(f"Erro no parsing do documento {file_path}: {e}")
            raise
    
    async def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse de PDF usando PyMuPDF"""
        try:
            # Tentar PyMuPDF primeiro
            return await self._parse_pdf_pymupdf(file_path)
        except Exception as e:
            logger.warning(f"PyMuPDF falhou para {file_path}: {e}")
            # Fallback para OCR
            return await self._parse_pdf_ocr(file_path)
    
    async def _parse_pdf_pymupdf(self, file_path: str) -> Dict[str, Any]:
        """Parse de PDF com PyMuPDF"""
        def _extract_text():
            doc = fitz.open(file_path)
            text_content = []
            metadata = {}
            
            # Extrair metadados
            metadata = doc.metadata
            
            # Extrair texto de cada página
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text()
                text_content.append({
                    "page": page_num + 1,
                    "text": text,
                    "char_count": len(text)
                })
            
            doc.close()
            return {
                "content": text_content,
                "metadata": metadata,
                "total_pages": doc.page_count,
                "method": "pymupdf"
            }
        
        # Executar em thread separada para timeout
        loop = asyncio.get_event_loop()
        return await asyncio.wait_for(
            loop.run_in_executor(None, _extract_text),
            timeout=self.pymupdf_timeout
        )
    
    async def _parse_pdf_ocr(self, file_path: str) -> Dict[str, Any]:
        """Parse de PDF com OCR (Tesseract)"""
        def _extract_with_ocr():
            doc = fitz.open(file_path)
            text_content = []
            
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                # Converter página para imagem
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                
                # OCR com Tesseract
                image = Image.open(io.BytesIO(img_data))
                text = pytesseract.image_to_string(
                    image, 
                    lang=self.ocr_language
                )
                
                text_content.append({
                    "page": page_num + 1,
                    "text": text,
                    "char_count": len(text)
                })
            
            doc.close()
            return {
                "content": text_content,
                "metadata": {"method": "ocr"},
                "total_pages": doc.page_count,
                "method": "tesseract"
            }
        
        loop = asyncio.get_event_loop()
        return await asyncio.wait_for(
            loop.run_in_executor(None, _extract_with_ocr),
            timeout=self.tesseract_timeout
        )
    
    async def _parse_image(self, file_path: str) -> Dict[str, Any]:
        """Parse de imagem com OCR"""
        def _extract_image_text():
            image = Image.open(file_path)
            text = pytesseract.image_to_string(
                image, 
                lang=self.ocr_language
            )
            
            return {
                "content": [{
                    "page": 1,
                    "text": text,
                    "char_count": len(text)
                }],
                "metadata": {"method": "ocr"},
                "total_pages": 1,
                "method": "tesseract"
            }
        
        loop = asyncio.get_event_loop()
        return await asyncio.wait_for(
            loop.run_in_executor(None, _extract_image_text),
            timeout=self.tesseract_timeout
        )
    
    async def _parse_text(self, file_path: str) -> Dict[str, Any]:
        """Parse de arquivo de texto"""
        def _extract_text():
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return {
                "content": [{
                    "page": 1,
                    "text": text,
                    "char_count": len(text)
                }],
                "metadata": {"method": "text"},
                "total_pages": 1,
                "method": "text"
            }
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _extract_text)
    
    async def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Parse de documento DOCX"""
        def _extract_docx():
            # TODO: Implementar parsing de DOCX
            # Usar python-docx library
            return {
                "content": [{
                    "page": 1,
                    "text": "DOCX parsing not implemented yet",
                    "char_count": 0
                }],
                "metadata": {"method": "docx"},
                "total_pages": 1,
                "method": "docx"
            }
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _extract_docx)
    
    async def validate_document(self, file_path: str) -> Dict[str, Any]:
        """Validar documento antes do parsing"""
        try:
            # Verificar se arquivo existe
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
            # Verificar tamanho do arquivo
            file_size = os.path.getsize(file_path)
            if file_size > settings.MAX_FILE_SIZE:
                raise ValueError(f"Arquivo muito grande: {file_size} bytes")
            
            # Verificar formato
            file_extension = file_path.split('.')[-1].lower()
            if file_extension not in self.supported_formats:
                raise ValueError(f"Formato não suportado: {file_extension}")
            
            return {
                "valid": True,
                "file_size": file_size,
                "format": file_extension,
                "message": "Documento válido"
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "message": "Documento inválido"
            }
