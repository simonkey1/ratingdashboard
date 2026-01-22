@echo off
echo ============================================
echo   Scraper de Ratings TV Chile
echo ============================================
echo.
echo Iniciando scraper en modo continuo...
echo Intervalo: 1 minuto (testing)
echo.
echo Los datos se guardaran en ratings_data.csv
echo Presiona Ctrl+C para detener
echo.

cd /d "%~dp0\.."
call venv\Scripts\activate

echo Ejecutando con intervalo de 1 minuto (testing)...
echo Para produccion (30 min), edita src\orchestrator.py linea 71
python src\orchestrator.py
