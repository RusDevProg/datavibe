from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from enum import Enum

class ChartType(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    AREA = "area"

class AnalysisRequest(BaseModel):
    data: List[Dict[str, Any]]
    text: Optional[str] = None

class AnalysisResponse(BaseModel):
    insight: str = Field(..., description="Главный инсайт в 2-3 предложениях")
    chart_type: ChartType = Field(..., description="Рекомендуемый тип графика")
    metrics: List[str] = Field(default=[], description="Ключевые метрики")
    summary: Dict[str, Any] = Field(default={}, description="Сводка по данным")
    recommendations: List[str] = Field(default=[], description="Рекомендации")
    chart_data: Optional[Dict[str, Any]] = Field(default=None, description="Данные для отрисовки графика (labels и datasets)")

class ChatRequest(BaseModel):
    message: str
    data: List[Dict[str, Any]]
    context: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str

class UploadResponse(BaseModel):
    success: bool
    filename: str
    rows: int
    columns: int
    preview: List[Dict[str, Any]]
    error: Optional[str] = None