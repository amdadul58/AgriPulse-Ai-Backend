from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
class ChunkService:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        text = ''
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages: text += page.extract_text() or ''
        return text
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        return splitter.split_text(text)
