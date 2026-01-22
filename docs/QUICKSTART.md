# Quick Start Guide

Esta guía te ayudará a poner en marcha el proyecto en menos de 5 minutos.

## 🚀 Instalación Rápida

### 1. Clonar y Configurar

```bash
# Clonar repositorio
git clone https://github.com/tuusuario/rating_scraping.git
cd rating_scraping

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
playwright install chromium
```

### 2. Ejecutar

**Dashboard:**
```bash
scripts\run_dashboard.bat
```

**Scraper:**
```bash
scripts\run_scraper.bat
```

## 📊 Acceder al Dashboard

Abre tu navegador en: **http://localhost:8501**

## 🎯 Próximos Pasos

- Ver [README.md](../README.md) para documentación completa
- Ver [DEPLOYMENT.md](DEPLOYMENT.md) para deploy en producción
- Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para contribuir

## ❓ Problemas Comunes

**Error: "playwright not found"**
```bash
playwright install chromium
```

**Error: "Port 8501 already in use"**
```bash
# Detener proceso anterior o usar otro puerto
streamlit run src/dashboard.py --server.port 8502
```

**Dashboard no muestra datos**
```bash
# Ejecutar scraper primero para generar datos
python scripts/test_scraper.py
```
