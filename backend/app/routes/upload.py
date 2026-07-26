from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.data_service import DataService
from app.models import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        df = await DataService.parse_file(file)
        preview = DataService.dataframe_to_json(df.head(5))
        
        return UploadResponse(
            success=True,
            filename=file.filename,
            rows=len(df),
            columns=len(df.columns),
            preview=preview
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))