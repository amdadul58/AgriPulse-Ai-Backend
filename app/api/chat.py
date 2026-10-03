from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.router_agent import RouterAgent

router = APIRouter(prefix='/chat', tags=['Chat'])

@router.post('/', response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        reply, source = await RouterAgent.process_input(
            chat_request.message, 
            db, 
            chat_request.image_base64
        )
        return ChatResponse(reply=reply, source=source)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
