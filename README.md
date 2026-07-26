# DataVibe — AI Dashboard

🚀 **AI-дашборд, который превращает сырые данные в инсайты**

DataVibe анализирует CSV/Excel файлы и автоматически генерирует AI-инсайты, визуализации и умный чат с данными.

**🌐 Live Demo:**
- Frontend: https://datavibe-gules.vercel.app
- Backend: https://datavibe-axk0.onrender.com
- GitHub: https://github.com/RusDevProg/datavibe

## ✨ Возможности

- **📥 Загрузка данных** — Drag-and-drop CSV/Excel или вставка текста
- ** AI-инсайты** — автоматическая генерация главных выводов
- **📈 Умные графики** — выбор оптимального типа визуализации
- **💬 Чат с данными** — задавайте вопросы и получайте ответы
- ** Современный UI** — glassmorphism, анимации, тёмная тема
- ** Приватность** — данные не сохраняются на сервере

## 🛠 Стек технологий

### Frontend
- **Vue 3** (Composition API)
- **Tailwind CSS** (glassmorphism эффекты)
- **Chart.js** + vue-chartjs
- **Vite** (сборка)
- **Axios** (HTTP клиент)

### Backend
- **FastAPI** (Python 3.11)
- **Pandas** (анализ данных)
- **HTTPX** (асинхронные запросы)
- **Pydantic** (валидация)

### AI
- **Cloudflare Workers AI** (Llama 3.1 8B)
- Бесплатный лимит: 10,000 запросов/день

### Деплой
- **Frontend**: Vercel
- **Backend**: Render (Free tier)

## 🚀 Быстрый старт

### Требования
- Python 3.10+
- Node.js 16+
- npm или yarn

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/RusDevProg/datavibe.git
cd datavibe
```
### 2. Настройте Backend

cd backend

# Создайте виртуальное окружение
python -m venv venv

# Активируйте (Windows)
venv\Scripts\activate

# Активируйте (Mac/Linux)
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте файл .env
notepad .env

Добавьте в .env:

CLOUDFLARE_API_TOKEN=your_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
API_MODEL=@cf/meta/llama-3.1-8b-instruct
DEBUG=True

Запустите сервер:

python run.py

Сервер запустится на: http://localhost:8000
Swagger документация: http://localhost:8000/docs

### 3. Настройте Frontend

Откройте новый терминал:

cd frontend

# Установите зависимости
npm install

# Создайте файл .env.local
notepad .env.local

Добавьте в .env.local:

VITE_API_URL=http://localhost:8000

Запустите dev-сервер:

npm run dev

Приложение откроется на: http://localhost:5173

## 📖 Как использовать

### 1. Загрузите файл
- Перетащите CSV/Excel файл в зону загрузки
- Или вставьте неструктурированный текст
- Нажмите **"Анализировать"**

### 2. Получите инсайт
- AI проанализирует данные
- Появится главный вывод
- Автоматически построится график

### 3. Задайте вопрос
- Используйте чат внизу
- Примеры вопросов:
  - `"Какой месяц самый прибыльный?"`
  - `"Расскажи про продажи в Москве"`
  - `"Какая средняя зарплата?"`

## 🔑 Получение API ключа Cloudflare

### 1. Зарегистрируйтесь
- Перейдите на https://dash.cloudflare.com/sign-up

### 2. Создайте API токен
- Перейдите в **Profile → API Tokens**
- Нажмите **"Create Token"**
- Выберите шаблон **"Edit Cloudflare Workers"** (или создайте кастомный с правами `Account → Workers AI → Read`)
- Нажмите **"Create Token"**
- Скопируйте полученный токен

### 3. Найдите Account ID
- Перейдите на https://dash.cloudflare.com/
- В правом нижнем углу найдите **"Account ID"**
- Скопируйте его

### 4. Добавьте в .env
- Откройте файл `.env` в папке `backend`
- Добавьте переменные:
  - `CLOUDFLARE_API_TOKEN=ваш_токен`
  - `CLOUDFLARE_ACCOUNT_ID=ваш_id`


## 📦 Деплой

### Frontend (Vercel)

#### 1. Подготовьте проект
- Залейте код на GitHub ✅

#### 2. Импортируйте в Vercel
- Перейдите на https://vercel.com/new
- Импортируйте репозиторий `datavibe`

#### 3. Настройте проект
- **Framework Preset:** `Vite`
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

#### 4. Добавьте переменные окружения
- **Key:** `VITE_API_URL`
- **Value:** URL вашего бэкенда (например, `https://datavibe-axk0.onrender.com`)

#### 5. Задеплойте
- Нажмите **Deploy**

### Backend (Render)

#### 1. Создайте Web Service
- Перейдите на https://render.com/
- Нажмите **New +** → **Web Service**
- Подключите GitHub и выберите репозиторий `datavibe`

#### 2. Настройте сервис
- **Name:** `datavibe-api`
- **Region:** Oregon (или Frankfurt)
- **Branch:** `main`
- **Root Directory:** `backend` ⚠️
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Instance Type:** `Free`

#### 3. Добавьте переменные окружения
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `API_MODEL=@cf/meta/llama-3.1-8b-instruct`

#### 4. Задеплойте
- Нажмите **Create Web Service**
- Подождите 2-3 минуты
- ✅ URL бэкенда: `https://datavibe-axk0.onrender.com`

---

## 🤖 Как я использовал ИИ

### 1. Cursor/Copilot — генерация кода
- Vue компоненты (`UploadZone.vue`, `ChartWidget.vue`)
- FastAPI роуты и Pydantic модели
- Tailwind CSS стили с glassmorphism эффектами

### 2. ChatGPT — архитектура и промпты
- Проектирование AI-сервисов на Python
- Написание эффективных промптов для анализа данных
- Оптимизация fallback-механизмов

### 3. Проблемы и решения
- **Проблема 1: AI возвращал кривой JSON**
  - *Решение:* Разделили логику — AI пишет только текст инсайта, а графики строим через Pandas
- **Проблема 2: Блокировки API (OpenAI/Google)**
  - *Решение:* Перешли на Cloudflare Workers AI — работает без VPN, 10к запросов/день бесплатно
- **Проблема 3: Python 3.14 на Render ломал pandas**
  - *Решение:* Добавили `runtime.txt` с Python 3.11 и упростили `requirements.txt`
- **Проблема 4: AI писал код вместо ответов в чате**
  - *Решение:* Преобразовали данные в CSV-формат и усилили промпт строгим запретом на генерацию кода

### 4. Что я узнал
- Как правильно структурировать промпты
- Когда использовать AI, а когда — традиционный код
- Как создавать устойчивые fallback механизмы
- Деплой full-stack приложений на бесплатных тарифах

---

## 📁 Структура проекта

```text
DATAVibe/
├── backend/                    # Бэкенд (Python/FastAPI)
│   ├── app/
│   │   ├── routes/             # API endpoints
│   │   │   ├── upload.py       # Загрузка файлов
│   │   │   ├── analyze.py      # AI анализ
│   │   │   └── chat.py         # Чат с данными
│   │   ├── services/
│   │   │   ├── ai_service.py   # Cloudflare AI
│   │   │   └── data_service.py # Парсинг CSV/Excel
│   │   ├── main.py             # FastAPI приложение
│   │   └── models.py           # Pydantic модели
│   ├── runtime.txt             # Python версия (3.11)
│   ├── requirements.txt        # Python зависимости
│   └── run.py                  # Точка входа
│
├── frontend/                   # Фронтенд (Vue 3)
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.vue  # Drag-and-drop
│   │   │   └── ChartWidget.vue # Графики
│   │   ├── api/
│   │   │   └── client.js       # API клиент
│   │   ├── App.vue             # Главный компонент
│   │   └── main.js             # Точка входа
│   └── package.json            # NPM зависимости
│
├── .gitignore                  # Игнорируемые файлы
└── README.md                   # Документация
```

## Автор

**Руслан**  
GitHub: [RusDevProg](https://github.com/RusDevProg)