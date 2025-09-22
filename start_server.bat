@echo off
cd /d "d:\banking_AI1\banking_AI"
echo Starting Banking AI FastAPI server on port 8080...
D:\banking_AI1\banking_AI\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
pause