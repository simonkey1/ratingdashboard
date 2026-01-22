# 🚀 Guía de Deployment - Render + Supabase

Esta guía te llevará paso a paso para deployar el Rating Scraper en producción usando Render y Supabase.

## 📋 Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Prerrequisitos](#prerrequisitos)
- [Paso 1: Configurar Supabase](#paso-1-configurar-supabase)
- [Paso 2: Preparar el Código](#paso-2-preparar-el-código)
- [Paso 3: Deploy en Render](#paso-3-deploy-en-render)
- [Paso 4: Configurar Variables de Entorno](#paso-4-configurar-variables-de-entorno)
- [Paso 5: Verificar Deployment](#paso-5-verificar-deployment)
- [Troubleshooting](#troubleshooting)

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND                          │
│  ┌───────────────────────────────────────────┐     │
│  │  Streamlit Dashboard (Render Web Service) │     │
│  │  - URL: https://tu-app.onrender.com       │     │
│  └─────────────────┬─────────────────────────┘     │
└────────────────────┼────────────────────────────────┘
                     │ Supabase Client
┌────────────────────┼────────────────────────────────┐
│                 DATABASE                            │
│  ┌─────────────────▼─────────────────────────┐     │
│  │  Supabase PostgreSQL                      │     │
│  │  - Tabla: ratings                         │     │
│  │  - RLS Policies                           │     │
│  └───────────────────────────────────────────┘     │
│                    ▲                                │
│                    │ INSERT                         │
│  ┌─────────────────┴─────────────────────────┐     │
│  │  Scraper (Render Background Worker)       │     │
│  │  - Playwright                             │     │
│  │  - Cron: cada 30 min                      │     │
│  └───────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

## Prerrequisitos

- [ ] Cuenta en [Supabase](https://supabase.com) (gratis)
- [ ] Cuenta en [Render](https://render.com) (gratis)
- [ ] Cuenta en [GitHub](https://github.com) (gratis)
- [ ] Código subido a GitHub

## Paso 1: Configurar Supabase

### 1.1 Crear Proyecto

1. Ir a [Supabase Dashboard](https://app.supabase.com)
2. Click en "New Project"
3. Configurar:
   - **Name**: `rating-scraper`
   - **Database Password**: Genera una contraseña segura (guárdala)
   - **Region**: Closest to your users (ej: `South America (São Paulo)`)
4. Click "Create new project"
5. Esperar 2-3 minutos mientras se crea

### 1.2 Crear Tabla

1. En el dashboard, ir a **SQL Editor**
2. Ejecutar el siguiente SQL:

```sql
-- Crear tabla de ratings
CREATE TABLE ratings (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ NOT NULL,
  chv FLOAT NOT NULL,
  canal13 FLOAT NOT NULL,
  tvm FLOAT NOT NULL,
  tvno FLOAT NOT NULL,
  lared FLOAT NOT NULL,
  mega FLOAT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Crear índice para búsquedas rápidas
CREATE INDEX idx_ratings_timestamp ON ratings(timestamp DESC);

-- Habilitar RLS (Row Level Security)
ALTER TABLE ratings ENABLE ROW LEVEL SECURITY;

-- Política para lectura pública
CREATE POLICY "Allow public read access"
ON ratings FOR SELECT
USING (true);

-- Política para inserción (solo con service_role key)
CREATE POLICY "Allow service role insert"
ON ratings FOR INSERT
WITH CHECK (true);
```

### 1.3 Obtener Credenciales

1. Ir a **Project Settings** → **API**
2. Copiar:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - **service_role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (⚠️ Secreto)

## Paso 2: Preparar el Código

### 2.1 Instalar Supabase Client

```bash
pip install supabase
```

### 2.2 Actualizar `requirements.txt`

Agregar:
```
supabase==2.3.0
```

### 2.3 Crear `src/supabase_client.py`

```python
import os
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """Crea y retorna cliente de Supabase"""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configurados")
    
    return create_client(url, key)
```

### 2.4 Actualizar `src/transformer.py`

Agregar método para guardar en Supabase:

```python
from supabase_client import get_supabase_client

class Transformer:
    # ... métodos existentes ...
    
    @staticmethod
    def save_to_supabase(data: Dict[str, any]):
        """Guarda datos en Supabase"""
        supabase = get_supabase_client()
        
        supabase.table('ratings').insert({
            'timestamp': data['TIMESTAMP'],
            'chv': data['CHV'],
            'canal13': data['CANAL13'],
            'tvm': data['TVM'],
            'tvno': data['TVNO'],
            'lared': data['LARED'],
            'mega': data['MEGA']
        }).execute()
```

### 2.5 Actualizar `src/orchestrator.py`

```python
# En run_single_scrape(), después de transform:
transformed_data = self.transformer.transform_ratings(ratings)

# Guardar en Supabase (producción) o CSV (local)
if os.getenv('ENVIRONMENT') == 'production':
    self.transformer.save_to_supabase(transformed_data)
else:
    self.transformer.append_to_csv(transformed_data, self.csv_filepath)
```

### 2.6 Actualizar `src/dashboard.py`

```python
from supabase_client import get_supabase_client

@st.cache_data(ttl=REFRESH_INTERVAL * 60)
def load_data():
    """Carga datos desde Supabase o CSV"""
    if os.getenv('ENVIRONMENT') == 'production':
        supabase = get_supabase_client()
        response = supabase.table('ratings')\
            .select('*')\
            .order('timestamp', desc=True)\
            .limit(1000)\
            .execute()
        
        df = pd.DataFrame(response.data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Renombrar columnas a mayúsculas
        df.columns = [col.upper() for col in df.columns]
        return df
    else:
        # Código existente para CSV
        ...
```

## Paso 3: Deploy en Render

### 3.1 Crear `render.yaml`

Crear en la raíz del proyecto:

```yaml
services:
  # Dashboard (Web Service)
  - type: web
    name: rating-dashboard
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run src/dashboard.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_ANON_KEY
        sync: false
  
  # Scraper (Background Worker)
  - type: worker
    name: rating-scraper
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt && playwright install chromium
    startCommand: python src/orchestrator.py
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
```

### 3.2 Push a GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 3.3 Conectar Render

1. Ir a [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Blueprint"
3. Conectar tu repositorio de GitHub
4. Render detectará `render.yaml` automáticamente
5. Click "Apply"

## Paso 4: Configurar Variables de Entorno

### 4.1 Dashboard (Web Service)

En Render Dashboard → `rating-dashboard` → Environment:

```
ENVIRONMENT=production
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4.2 Scraper (Background Worker)

En Render Dashboard → `rating-scraper` → Environment:

```
ENVIRONMENT=production
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (service_role)
```

⚠️ **Importante**: El scraper usa `SUPABASE_KEY` (service_role), no anon key.

## Paso 5: Verificar Deployment

### 5.1 Verificar Dashboard

1. Ir a la URL de tu dashboard: `https://rating-dashboard.onrender.com`
2. Verificar que carga sin errores
3. Verificar que muestra datos (si ya hay datos en Supabase)

### 5.2 Verificar Scraper

1. En Render Dashboard → `rating-scraper` → Logs
2. Verificar que el scraper está ejecutándose
3. Verificar que no hay errores
4. Verificar en Supabase que se están insertando datos

### 5.3 Verificar Datos en Supabase

1. Ir a Supabase Dashboard → Table Editor → `ratings`
2. Verificar que hay registros nuevos
3. Verificar que los timestamps son recientes

## Troubleshooting

### Error: "Port already in use"

**Solución**: Render asigna el puerto automáticamente via `$PORT`. Asegúrate de usar:
```python
streamlit run src/dashboard.py --server.port=$PORT
```

### Error: "playwright not found"

**Solución**: Agregar a `buildCommand` en `render.yaml`:
```yaml
buildCommand: pip install -r requirements.txt && playwright install chromium
```

### Error: "SUPABASE_URL not found"

**Solución**: Verificar que las variables de entorno están configuradas en Render Dashboard.

### Dashboard muestra "No data"

**Solución**: 
1. Verificar que el scraper está corriendo
2. Verificar logs del scraper en Render
3. Verificar que hay datos en Supabase

### Scraper falla con "chromium not found"

**Solución**: Agregar dependencias del sistema en `render.yaml`:
```yaml
buildCommand: |
  pip install -r requirements.txt
  playwright install-deps chromium
  playwright install chromium
```

## Costos

### Supabase (Free Tier)
- ✅ 500 MB de base de datos
- ✅ 2 GB de transferencia
- ✅ 50,000 usuarios activos mensuales

### Render (Free Tier)
- ✅ 750 horas/mes de Web Service
- ✅ 750 horas/mes de Background Worker
- ⚠️ Se duerme después de 15 min de inactividad
- ⚠️ Tarda ~30s en despertar

### Upgrade Recomendado (Opcional)

Para producción seria:
- **Render Starter**: $7/mes (sin sleep, más RAM)
- **Supabase Pro**: $25/mes (más storage, mejor performance)

## Mantenimiento

### Actualizar Código

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render auto-deploya automáticamente.

### Monitorear Logs

```bash
# Render CLI
render logs -s rating-dashboard
render logs -s rating-scraper
```

### Backup de Datos

Exportar desde Supabase:
```sql
COPY ratings TO '/tmp/ratings_backup.csv' CSV HEADER;
```

---

¿Preguntas? Abre un [issue en GitHub](https://github.com/tuusuario/rating_scraping/issues).
