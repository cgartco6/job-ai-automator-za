@echo off
echo Setting up AI Job Automator on Windows 10...
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv job_ai_venv
call job_ai_venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Setting up environment variables...
copy .env.example .env
echo Please edit .env file with your API keys
notepad .env

echo Initializing database...
python scripts/setup_db.py

echo Starting services...
echo Starting Redis...
start redis-server

echo Starting Celery worker...
start celery -A src.celery_app worker --pool=solo -l info

echo Starting main application...
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Application running at: http://localhost:8000
echo Owner Dashboard: http://localhost:8000/owners/dashboard
echo API Documentation: http://localhost:8000/docs
echo.
pause
