"""
Dashboard Streamlit para visualizar ratings de TV en tiempo real
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="📺 Ratings TV Chile - En Vivo",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    .update-time {
        color: #666;
        font-size: 14px;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración
CSV_FILE = "ratings_data.csv"
REFRESH_INTERVAL = 30  # minutos
CHANNEL_COLORS = {
    'CHV': '#FF6B6B',
    'CANAL13': '#4ECDC4',
    'TVM': '#45B7D1',
    'TVNO': '#FFA07A',
    'LARED': '#98D8C8',
    'MEGA': '#6C5CE7'
}

CHANNEL_NAMES = {
    'CHV': 'Chilevisión',
    'CANAL13': 'Canal 13',
    'TVM': 'TVN',  # El slug 'tvm' corresponde al canal TVN
    'TVNO': 'TV+',
    'LARED': 'La Red',
    'MEGA': 'Mega'
}


@st.cache_data(ttl=REFRESH_INTERVAL * 60)
def load_data():
    """Carga los datos del CSV con cache"""
    try:
        df = pd.read_csv(CSV_FILE)
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
        return df
    except FileNotFoundError:
        st.error(f"⚠️ No se encontró el archivo {CSV_FILE}. Ejecuta el scraper primero.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        return pd.DataFrame()


def get_latest_ratings(df):
    """Obtiene los ratings más recientes"""
    if df.empty:
        return {}
    latest = df.iloc[-1]
    return {col: latest[col] for col in df.columns if col != 'TIMESTAMP'}


def create_current_ratings_chart(df):
    """Crea gráfico de barras con ratings actuales"""
    if df.empty:
        return None
    
    latest_ratings = get_latest_ratings(df)
    
    # Preparar datos
    channels = [CHANNEL_NAMES.get(ch, ch) for ch in latest_ratings.keys()]
    values = list(latest_ratings.values())
    colors = [CHANNEL_COLORS.get(ch, '#999') for ch in latest_ratings.keys()]
    
    # Crear gráfico
    fig = go.Figure(data=[
        go.Bar(
            x=channels,
            y=values,
            marker_color=colors,
            text=values,
            textposition='outside',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{x}</b><br>Rating: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': '📊 Ratings Actuales por Canal',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': 'white'}
        },
        xaxis_title="Canal",
        yaxis_title="Rating",
        template="plotly_dark",
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig


def create_timeline_chart(df):
    """Crea gráfico de líneas con evolución temporal"""
    if df.empty or len(df) < 2:
        return None
    
    fig = go.Figure()
    
    for col in df.columns:
        if col != 'TIMESTAMP':
            fig.add_trace(go.Scatter(
                x=df['TIMESTAMP'],
                y=df[col],
                mode='lines+markers',
                name=CHANNEL_NAMES.get(col, col),
                line=dict(color=CHANNEL_COLORS.get(col, '#999'), width=3),
                marker=dict(size=8),
                hovertemplate='<b>%{fullData.name}</b><br>%{x}<br>Rating: %{y}<extra></extra>'
            ))
    
    fig.update_layout(
        title={
            'text': '📈 Evolución de Ratings en el Tiempo',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': 'white'}
        },
        xaxis_title="Fecha y Hora",
        yaxis_title="Rating",
        template="plotly_dark",
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig


def create_share_pie_chart(df):
    """Crea gráfico de torta con share de audiencia"""
    if df.empty:
        return None
    
    latest_ratings = get_latest_ratings(df)
    total = sum(latest_ratings.values())
    
    if total == 0:
        return None
    
    # Calcular porcentajes
    labels = [CHANNEL_NAMES.get(ch, ch) for ch in latest_ratings.keys()]
    values = list(latest_ratings.values())
    colors = [CHANNEL_COLORS.get(ch, '#999') for ch in latest_ratings.keys()]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>Rating: %{value}<br>Share: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '🥧 Share de Audiencia',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': 'white'}
        },
        template="plotly_dark",
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig


def main():
    # Header
    st.title("📺 Ratings TV Chile - Dashboard en Vivo")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        st.info("🔄 Los datos se actualizan automáticamente cada 30 minutos")
        
        st.markdown("---")
        
        # Información del archivo
        if Path(CSV_FILE).exists():
            file_size = Path(CSV_FILE).stat().st_size
            st.success(f"✅ Archivo CSV encontrado")
            st.caption(f"Tamaño: {file_size:,} bytes")
        else:
            st.error(f"❌ Archivo no encontrado")
        
        st.markdown("---")
        
        # Manual refresh
        if st.button("🔄 Actualizar Ahora", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Cargar datos
    df = load_data()
    
    if df.empty:
        st.warning("⚠️ No hay datos disponibles. Asegúrate de que el scraper esté ejecutándose.")
        st.stop()
    
    # Información de última actualización
    last_update = df['TIMESTAMP'].iloc[-1]
    total_records = len(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Última Actualización", last_update.strftime("%d/%m/%Y %H:%M:%S"))
    with col2:
        st.metric("📊 Total de Registros", f"{total_records:,}")
    with col3:
        time_range = df['TIMESTAMP'].max() - df['TIMESTAMP'].min()
        hours = time_range.total_seconds() / 3600
        st.metric("⏱️ Rango de Datos", f"{hours:.1f} horas")
    
    st.markdown("---")
    
    # Métricas de ratings actuales
    st.subheader("🎯 Ratings Actuales")
    latest_ratings = get_latest_ratings(df)
    
    cols = st.columns(len(latest_ratings))
    for idx, (channel, rating) in enumerate(latest_ratings.items()):
        with cols[idx]:
            # Calcular delta si hay datos previos
            delta = None
            if len(df) > 1:
                prev_rating = df.iloc[-2][channel]
                delta = rating - prev_rating
            
            st.metric(
                label=CHANNEL_NAMES.get(channel, channel),
                value=f"{rating}",
                delta=f"{delta:+.1f}" if delta is not None else None,
                delta_color="normal"
            )
    
    st.markdown("---")
    
    # Gráficos
    tab1, tab2, tab3 = st.tabs(["📊 Ratings Actuales", "📈 Evolución Temporal", "🥧 Share de Audiencia"])
    
    with tab1:
        chart1 = create_current_ratings_chart(df)
        if chart1:
            st.plotly_chart(chart1, use_container_width=True)
    
    with tab2:
        chart2 = create_timeline_chart(df)
        if chart2:
            st.plotly_chart(chart2, use_container_width=True)
        else:
            st.info("📊 Se necesitan al menos 2 registros para mostrar la evolución temporal")
    
    with tab3:
        chart3 = create_share_pie_chart(df)
        if chart3:
            st.plotly_chart(chart3, use_container_width=True)
        else:
            st.warning("⚠️ No hay datos suficientes para calcular el share")
    
    st.markdown("---")
    
    # Tabla de datos recientes
    with st.expander("📋 Ver Datos Recientes (últimos 10 registros)"):
        recent_df = df.tail(10).copy()
        recent_df['TIMESTAMP'] = recent_df['TIMESTAMP'].dt.strftime('%d/%m/%Y %H:%M:%S')
        st.dataframe(recent_df.iloc[::-1], use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
