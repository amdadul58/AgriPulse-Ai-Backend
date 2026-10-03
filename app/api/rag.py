from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.rag.rag_service import RAGService

router = APIRouter(prefix='/rag', tags=['RAG'])

@router.post('/ask')
async def ask_rag(
    query: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    RAG (Retrieval Augmented Generation) ব্যবহার করে PDF ডকুমেন্ট থেকে উত্তর খুঁজে বের করে।
    """
    answer = await RAGService.ask(query)
    return {"query": query, "answer": answer}
