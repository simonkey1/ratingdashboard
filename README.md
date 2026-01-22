# 📺 Rating Scraper - Zapping TV Chile

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)
[![Playwright](https://img.shields.io/badge/Playwright-1.41.0-2EAD33.svg)](https://playwright.dev)

Sistema automatizado de web scraping para recolectar y visualizar ratings de canales de TV chilenos desde [Zapping](https://www.zapping.com/rating) con dashboard interactivo en tiempo real.

![Dashboard Preview](docs/screenshots/dashboard_preview.png)

## ✨ Características

- 🎯 **Scraping Automatizado**: Recolecta ratings de 6 canales chilenos (CHV, Canal 13, TVN, TV+, La Red, Mega)
- ⏰ **Polling Configurable**: Intervalo ajustable (default: 30 minutos)
- 💾 **Almacenamiento CSV**: Datos acumulativos con timestamps ISO 8601
- 📊 **Dashboard Interactivo**: Visualización en tiempo real con Streamlit y Plotly
- 🔄 **Actualización Manual**: Botón de refresh para obtener datos al instante
- 🛡️ **Manejo de Errores**: Sistema robusto con logging detallado
- 📈 **Múltiples Visualizaciones**: Gráficos de barras, líneas y torta
- 🌐 **Listo para Deploy**: Preparado para Render + Supabase

## 📁 Estructura del Proyecto

```
rating_scraping/
├── src/                        # Código fuente
│   ├── rating_scraper.py       # Scraper con Playwright
│   ├── transformer.py          # Transformación de datos
│   ├── orchestrator.py         # Coordinador del proceso
│   └── dashboard.py            # Dashboard Streamlit
│
├── scripts/                    # Scripts de utilidad
│   ├── test_scraper.py         # Test de scraping único
│   ├── debug_ratings.py        # Debug de valores
│   ├── run_dashboard.bat       # Lanzador dashboard (Windows)
│   └── run_scraper.bat         # Lanzador scraper (Windows)
│
├── docs/                       # Documentación
│   ├── DEPLOYMENT.md           # Guía de deployment
│   ├── API.md                  # Documentación de API
│   └── screenshots/            # Capturas del dashboard
│
├── .github/                    # Configuración GitHub
│   └── workflows/              # GitHub Actions
│
├── requirements.txt            # Dependencias de producción
├── .gitignore                  # Archivos ignorados
├── LICENSE                     # Licencia MIT
└── README.md                   # Este archivo
```

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tuusuario/rating_scraping.git
cd rating_scraping
```

2. **Crear entorno virtual**

```bash
python -m venv venv
```

3. **Activar entorno virtual**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

5. **Instalar navegador Chromium**

```bash
playwright install chromium
```

### Uso

#### Opción 1: Scripts BAT (Windows - Recomendado)

**Dashboard:**
```bash
scripts\run_dashboard.bat
```

**Scraper:**
```bash
scripts\run_scraper.bat
```

#### Opción 2: Comandos Python

**Dashboard:**
```bash
streamlit run src/dashboard.py
```

**Scraper (testing - 1 minuto):**
```bash
python src/orchestrator.py
```

**Scraper (producción - 30 minutos):**

Editar `src/orchestrator.py` línea 71:
```python
orchestrator.run_continuous(interval_minutes=30)
```

## 📊 Dashboard

El dashboard incluye:

- **📈 Gráfico de Barras**: Ratings actuales por canal
- **📉 Gráfico de Líneas**: Evolución temporal
- **🥧 Gráfico de Torta**: Share de audiencia
- **📊 Métricas en Tiempo Real**: Con deltas de cambio
- **🔄 Actualización Manual**: Botón de refresh
- **📋 Tabla de Datos**: Últimos 10 registros

**Acceso**: http://localhost:8501

## 📦 Dependencias

### Producción

- `playwright==1.41.0` - Web scraping
- `pandas==2.2.0` - Manipulación de datos
- `streamlit==1.31.0` - Dashboard web
- `plotly==5.18.0` - Gráficos interactivos

### Desarrollo

Ver `requirements-dev.txt` para dependencias de desarrollo.

## 🔧 Configuración

### Canales Soportados

| Canal | Slug API | Nombre Display |
|-------|----------|----------------|
| CHV | `chv` | Chilevisión |
| CANAL13 | `13` | Canal 13 |
| TVM | `tvm` | TVN |
| TVNO | `tvno` | TV+ |
| LARED | `lared` | La Red |
| MEGA | `mega` | Mega |

### Formato de Datos

El CSV generado tiene el siguiente formato:

```csv
TIMESTAMP,CHV,CANAL13,TVM,TVNO,LARED,MEGA
2026-01-21T23:51:26.018770,39.4,23.1,0.6,12.1,0.2,24.7
```

- **TIMESTAMP**: ISO 8601 format
- **Ratings**: Float con decimales preservados

## 🌐 Deployment

### Render + Supabase (Recomendado)

Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para guía completa de deployment.

**Resumen**:
1. Crear proyecto en Supabase
2. Configurar tabla `ratings`
3. Deploy dashboard en Render (Web Service)
4. Deploy scraper en Render (Background Worker)

### Alternativas

- **Heroku**: Web dyno + Worker dyno
- **Railway**: Similar a Render
- **DigitalOcean App Platform**: Con PostgreSQL managed

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [Zapping](https://www.zapping.com) por proporcionar los datos de ratings
- [Playwright](https://playwright.dev) por la excelente herramienta de scraping
- [Streamlit](https://streamlit.io) por el framework de dashboard

## 📧 Contacto

Tu Nombre - [@tutwitter](https://twitter.com/tutwitter)

Link del Proyecto: [https://github.com/tuusuario/rating_scraping](https://github.com/tuusuario/rating_scraping)

## 🗺️ Roadmap

- [ ] API REST para consultar datos
- [ ] Autenticación para dashboard
- [ ] Alertas por email/Telegram
- [ ] Exportar a Excel
- [ ] Frontend alternativo en SvelteKit
- [ ] Soporte para más canales
- [ ] Análisis predictivo con ML

---

**Hecho con ❤️ en Chile** 🇨🇱
