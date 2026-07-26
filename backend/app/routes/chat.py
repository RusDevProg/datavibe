from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_data(request: ChatRequest):
    try:
        if not request.data:
            raise HTTPException(status_code=400, detail="No data loaded")
        
        reply = await ai_service.chat_with_data(
            request.message,
            request.data,
            request.context
        )
        
        return ChatResponse(reply=reply)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))