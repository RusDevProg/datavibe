import json
import os
import re
from typing import List, Dict, Any
import httpx
import pandas as pd
from app.models import AnalysisResponse, ChartType


class AIService:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        
        # Cloudflare Workers AI
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        
        # Для совместимости с остальным кодом
        self.api_key = self.api_token
        
        self.model = os.getenv("API_MODEL", "@cf/meta/llama-3.1-8b-instruct")
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run"
        
        print("=" * 50)
        print("🔧 AI SERVICE CONFIGURATION:")
        print(f"  API Key loaded: {'✅ YES' if self.api_key else '❌ NO'}")
        print(f"  API Key length: {len(self.api_key) if self.api_key else 0}")
        print(f"  Account ID: {self.account_id}")
        print(f"  Model: {self.model}")
        print(f"  Base URL: {self.base_url}")
        print("=" * 50)
    
    def _data_to_text(self, data: List[Dict[str, Any]]) -> str:
        """Преобразуем данные в читаемый табличный текст"""
        if not data:
            return "Данные отсутствуют"
        
        df = pd.DataFrame(data)
        
        # Создаём текстовое представление как таблица
        lines = []
        headers = list(df.columns)
        lines.append(" | ".join(headers))
        lines.append("-" * 60)
        
        for _, row in df.head(50).iterrows():
            line = " | ".join([str(row[col]) for col in headers])
            lines.append(line)
        
        return "\n".join(lines)
    
    async def analyze_data(self, data: List[Dict[str, Any]], text: str = None) -> AnalysisResponse:
        """Анализ данных: AI пишет инсайт, график строим через Pandas"""
        data_text = self._data_to_text(data) if data else text
        
        if not data_text:
            return self._get_fallback_analysis([])
        
        if not self.api_key:
            print("⚠️ API ключ не найден, используем fallback")
            return self._get_fallback_analysis(data)
        
        # УСИЛЕННЫЙ ПРОМПТ — строгое требование русского языка
        prompt = f"""Проанализируй данные ниже и напиши ГЛАВНЫЙ ИНСАЙТ в 2-3 предложениях.

ДАННЫЕ:
{data_text}

ВАЖНО:
- Отвечай ТОЛЬКО на русском языке
- НЕ используй английские слова
- НЕ пиши "Главный инсайт:" — просто напиши текст
- Найди самую важную закономерность или вывод

ИНСАЙТ:"""

        try:
            print(f"📡 Отправляю запрос к AI за инсайтом...")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/{self.model}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "messages": [
                            {"role": "system", "content": "Отвечай ТОЛЬКО на русском языке. Никакого английского."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    }
                )
                
                print(f"📊 Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"❌ AI Error: {response.text[:200]}")
                    return self._get_fallback_analysis(data)
                
                result = response.json()
                insight = result.get("result", {}).get("response", "").strip()
                print(f"✅ AI Insight: {insight[:200]}...")
                
                # Проверяем что инсайт на русском (нет английских слов)
                english_words = re.findall(r'\b[a-zA-Z]{4,}\b', insight)
                if len(english_words) > 2:
                    print(f"⚠️ Инсайт содержит английский: {english_words}")
                    return self._get_fallback_analysis(data)
                
                if not insight:
                    return self._get_fallback_analysis(data)
                
                chart_info = self._build_chart_from_data(data)
                
                return AnalysisResponse(
                    insight=insight,
                    chart_type=chart_info["chart_type"],
                    metrics=chart_info["metrics"],
                    summary={},
                    recommendations=["Используйте чат ниже, чтобы задать вопрос по этим данным"],
                    chart_data=chart_info["chart_data"]
                )
                
        except Exception as e:
            print(f"❌ AI Exception: {type(e).__name__}: {e}")
            return self._get_fallback_analysis(data)

    def _build_chart_from_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Строит график через Pandas — всегда работает"""
        if not data:
            return {
                "chart_type": ChartType.BAR,
                "metrics": [],
                "chart_data": {"labels": [], "datasets": []}
            }
        
        df = pd.DataFrame(data)
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        chart_data = {"labels": [], "datasets": []}
        chart_type = ChartType.BAR
        metrics = numeric_cols[:5] if numeric_cols else categorical_cols[:5]
        
        if numeric_cols and len(df) > 0:
            col = numeric_cols[0]
            label_col = categorical_cols[0] if categorical_cols else None
            
            if label_col:
                labels = df[label_col].head(10).tolist()
            else:
                labels = [f"Запись {i+1}" for i in range(min(10, len(df)))]
            
            chart_data = {
                "labels": labels,
                "datasets": [{
                    "label": col,
                    "data": df[col].head(10).fillna(0).tolist()
                }]
            }
            chart_type = ChartType.BAR
        
        elif categorical_cols and len(df) > 0:
            col = categorical_cols[0]
            counts = df[col].value_counts().head(5)
            chart_data = {
                "labels": counts.index.tolist(),
                "datasets": [{
                    "label": f"Количество по {col}",
                    "data": counts.values.tolist()
                }]
            }
            chart_type = ChartType.PIE
        
        return {
            "chart_type": chart_type,
            "metrics": metrics,
            "chart_data": chart_data
        }

    def _get_fallback_analysis(self, data: List[Dict[str, Any]]) -> AnalysisResponse:
        """Запасной вариант если AI не сработал"""
        if not data:
            return AnalysisResponse(
                insight="Недостаточно данных для анализа.",
                chart_type=ChartType.BAR,
                metrics=[],
                summary={},
                recommendations=["Загрузите файл с данными"],
                chart_data={"labels": [], "datasets": []}
            )
        
        df = pd.DataFrame(data)
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        insight = f"Успешно загружено {len(df)} записей и {len(df.columns)} колонок. "
        if numeric_cols:
            insight += f"Обнаружены числовые показатели: {', '.join(numeric_cols[:2])}."
        
        chart_info = self._build_chart_from_data(data)
        
        return AnalysisResponse(
            insight=insight,
            chart_type=chart_info["chart_type"],
            metrics=chart_info["metrics"],
            summary={},
            recommendations=["Используйте чат ниже, чтобы задать вопрос по этим данным"],
            chart_data=chart_info["chart_data"]
        )

    async def chat_with_data(self, message: str, data: List[Dict[str, Any]], context: str = None) -> str:
        """Чат с данными — используем табличный формат"""
        data_text = self._data_to_text(data)
        
        if not self.api_key:
            return self._fallback_chat_response(message, data)
        
        # ОЧЕНЬ ЧЁТКИЙ ПРОМПТ
        prompt = f"""Ты аналитик. Отвечай на вопрос ПОЛЬЗОВАТЕЛЯ используя данные ниже.

ДАННЫЕ (таблица):
{data_text}

ПРАВИЛА:
- Отвечай на русском языке
- Используй цифры из таблицы
- НЕ пиши код
- НЕ объясняй как считать
- Просто дай ответ

ВОПРОС: {message}

ОТВЕТ:"""

        try:
            print(f"💬 Chat запрос: {message[:50]}...")
            print(f"📊 Данных в таблице: {len(data)} строк")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/{self.model}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "messages": [
                            {"role": "system", "content": "Ты аналитик данных. Отвечай на русском языке, конкретно, с цифрами."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3
                    }
                )
                
                print(f"💬 Chat Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"❌ Chat Error: {response.text[:200]}")
                    return self._fallback_chat_response(message, data)
                
                result = response.json()
                reply = result.get("result", {}).get("response", "").strip()
                print(f"✅ Chat Response: {reply[:200]}...")
                
                # Проверяем что AI не пишет код
                if "python" in reply.lower() or "```" in reply or len(reply) < 10:
                    print("️ AI пишет код или пустой ответ, используем fallback")
                    return self._fallback_chat_response(message, data)
                
                return reply
                
        except Exception as e:
            print(f"❌ Chat Exception: {type(e).__name__}: {e}")
            return self._fallback_chat_response(message, data)

    def _fallback_chat_response(self, message: str, data: List[Dict[str, Any]]) -> str:
        """Умный fallback для чата без AI"""
        if not data:
            return "Данные не загружены. Пожалуйста, загрузите файл."
        
        df = pd.DataFrame(data)
        message_lower = message.lower()
        
        # Про конкретный регион
        if "москв" in message_lower or "питербург" in message_lower or "казан" in message_lower:
            region_col = next((c for c in df.columns if 'регион' in c.lower() or 'город' in c.lower()), None)
            if region_col:
                for region in df[region_col].unique():
                    if region.lower() in message_lower:
                        region_df = df[df[region_col] == region]
                        revenue = region_df['Выручка'].sum() if 'Выручка' in region_df.columns else 0
                        orders = region_df['Заказы'].sum() if 'Заказы' in region_df.columns else 0
                        categories = region_df['Категория'].unique().tolist() if 'Категория' in region_df.columns else []
                        return f"Продажи в {region}:\n• Выручка: {revenue:,.0f} руб.\n• Заказы: {orders}\n• Категории: {', '.join(categories)}"
        
        # Про самый прибыльный месяц
        if "самый прибыльный" in message_lower or "лучший месяц" in message_lower:
            if 'Выручка' in df.columns and 'Месяц' in df.columns:
                best_month = df.loc[df['Выручка'].idxmax()]
                return f"Самый прибыльный месяц — {best_month.get('Месяц', 'неизвестно')} с выручкой {best_month.get('Выручка', 0):,.0f} руб. и {best_month.get('Заказы', 0)} заказами."
        
        # Про средний чек
        if "средний чек" in message_lower:
            month_match = next((m for m in ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'] if m in message_lower), None)
            if month_match and 'Месяц' in df.columns:
                month_df = df[df['Месяц'].str.lower() == month_match]
                if len(month_df) > 0:
                    if 'Средний_чек' in month_df.columns:
                        avg = month_df['Средний_чек'].mean()
                        return f"Средний чек в {month_match.capitalize()}: {avg:,.0f} руб."
                    elif 'Выручка' in month_df.columns and 'Заказы' in month_df.columns:
                        revenue = month_df['Выручка'].sum()
                        orders = month_df['Заказы'].sum()
                        avg = revenue / orders if orders > 0 else 0
                        return f"Средний чек в {month_match.capitalize()}: {avg:,.0f} руб."
        
        # Про сезонность
        if "сезон" in message_lower:
            if 'Выручка' in df.columns and 'Месяц' in df.columns:
                avg_monthly = df['Выручка'].mean()
                max_row = df.loc[df['Выручка'].idxmax()]
                min_row = df.loc[df['Выручка'].idxmin()]
                return f"Да, видна сезонность: пик продаж в {max_row.get('Месяц')} ({max_row.get('Выручка', 0):,.0f} руб.), минимум в {min_row.get('Месяц')} ({min_row.get('Выручка', 0):,.0f} руб.). Средняя выручка: {avg_monthly:,.0f} руб./мес."
        
        # Про категорию
        if "категор" in message_lower:
            if 'Категория' in df.columns and 'Выручка' in df.columns:
                cat_summary = df.groupby('Категория')['Выручка'].sum().sort_values(ascending=False)
                best_cat = cat_summary.index[0]
                return f"Лучшая категория — {best_cat} ({cat_summary.iloc[0]:,.0f} руб. выручки)."
        
        # Сколько записей
        if "сколько" in message_lower:
            return f"В данных {len(df)} записей и {len(df.columns)} колонок: {', '.join(df.columns)}."
        
        # Общий ответ
        return f"Данные содержат {len(df)} записей. Колонки: {', '.join(df.columns)}. Попробуйте спросить: 'какой месяц самый прибыльный?', 'расскажи про Москву'."