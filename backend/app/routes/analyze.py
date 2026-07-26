from fastapi import APIRouter, HTTPException
from app.models import AnalysisRequest, AnalysisResponse
from app.services.ai_service import AIService
from app.services.data_service import DataService

router = APIRouter()
ai_service = AIService()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_data(request: AnalysisRequest):
    try:
        if not request.data and not request.text:
            raise HTTPException(status_code=400, detail="No data provided")
        
        if request.text and not request.data:
            df = DataService.parse_text_data(request.text)
            request.data = DataService.dataframe_to_json(df)
        
        analysis = await ai_service.analyze_data(request.data, request.text)
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))