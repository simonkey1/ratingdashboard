@echo off
echo ============================================
echo   Dashboard de Ratings TV Chile
echo ============================================
echo.
echo Iniciando Streamlit...
echo.
echo El dashboard se abrira automaticamente en tu navegador
echo Presiona Ctrl+C para detener
echo.

cd /d "%~dp0\.."
call venv\Scripts\activate
streamlit run src\dashboard.py
