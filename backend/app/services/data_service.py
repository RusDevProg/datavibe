import pandas as pd
import io
import json
from typing import List, Dict, Any, Optional
from fastapi import UploadFile

class DataService:
    @staticmethod
    async def parse_file(file: UploadFile) -> pd.DataFrame:
        content = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise ValueError("Unsupported file format")
        
        return df
    
    @staticmethod
    def dataframe_to_json(df: pd.DataFrame) -> List[Dict[str, Any]]:
        return df.replace({pd.NA: None, float('nan'): None}).to_dict('records')
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_columns": df.select_dtypes(include=['float64', 'int64']).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object', 'category']).columns.tolist(),
            "missing_values": df.isnull().sum().to_dict(),
            "statistics": {}
        }
        
        for col in summary["numeric_columns"]:
            summary["statistics"][col] = {
                "mean": float(df[col].mean()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "std": float(df[col].std())
            }
        
        return summary
    
    @staticmethod
    def parse_text_data(text: str) -> pd.DataFrame:
        lines = text.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("Текст должен содержать заголовки и данные")
        
        import re
        first_line = lines[0]
        separators = ['\t', ',', ';', '|']
        sep = next((s for s in separators if s in first_line), None)
        
        if not sep:
            data = [line.split() for line in lines]
            headers = data[0]
            rows = data[1:]
        else:
            data = [line.split(sep) for line in lines]
            headers = data[0]
            rows = data[1:]
        
        df = pd.DataFrame(rows, columns=headers)
        
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                pass
        
        return df