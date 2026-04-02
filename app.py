import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text, inspect
import re
import io
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="LadyGlow ERP", layout="wide", page_icon="✦")

# =====================================================================
# 🎨 TEMA VISUAL — ROSE GOLD · MAUVE · CREAM
# =====================================================================
st.html("""
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Nunito:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
    --rose:        #C49A6C;
    --rose-dark:   #A07845;
    --rose-light:  #EDD5BE;
    --rose-faint:  #FAF0E8;
    --mauve:       #9B7EA6;
    --mauve-light: #D8C8E3;
    --cream:       #FDF8F3;
    --cream-dark:  #F0E6DC;
    --border:      #E2D0C0;
    --dark:        #2D2020;
    --text:        #4A3838;
    --muted:       #9A8A8A;
    --white:       #FFFFFF;
    --green:       #7BAE8A;
    --red:         #C47878;
}

/* === GLOBAL === */
html, body, .stApp, * {
    font-family: 'Nunito', sans-serif !important;
}
.stApp { background-color: var(--cream) !important; }
.main .block-container {
    padding: 1.8rem 2.5rem 3rem !important;
    max-width: 1400px !important;
}

/* === TYPOGRAPHY === */
h1 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--dark) !important;
    font-weight: 400 !important;
    letter-spacing: -0.5px !important;
    font-size: 2.1rem !important;
}
h2, h3 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text) !important;
    font-weight: 400 !important;
}
.stMarkdown p { color: var(--text); line-height: 1.6; }

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #FEF1E6 0%, #F5E6D5 55%, #EDD8C5 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span { color: var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stSlider { background: transparent !important; }
[data-testid="stSidebar"] hr { border-color: var(--border) !important; }

/* === BUTTONS — Primary === */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--rose) 0%, var(--rose-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2px !important;
    padding: 0.55rem 1.6rem !important;
    box-shadow: 0 4px 18px rgba(196,154,108,0.35) !important;
    transition: all 0.25s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 28px rgba(196,154,108,0.5) !important;
}
.stButton > button[kind="primary"]:active { transform: translateY(0) !important; }

/* === BUTTONS — Secondary === */
.stButton > button:not([kind="primary"]) {
    border: 2px solid var(--rose) !important;
    color: var(--rose) !important;
    border-radius: 10px !important;
    background: transparent !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: var(--rose-faint) !important;
}

/* === FORM SUBMIT BUTTONS === */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--rose) 0%, var(--rose-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 0.55rem 1.6rem !important;
    box-shadow: 0 4px 18px rgba(196,154,108,0.35) !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 28px rgba(196,154,108,0.5) !important;
}

/* === METRICS === */
[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.4rem !important;
    box-shadow: 0 2px 18px rgba(0,0,0,0.06) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 26px rgba(0,0,0,0.1) !important;
}
[data-testid="stMetricLabel"] p {
    font-size: 0.70rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.9px !important;
    color: var(--muted) !important;
    font-weight: 700 !important;
    margin-bottom: 0.2rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.65rem !important;
    color: var(--dark) !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricDelta"] { font-size: 0.76rem !important; font-weight: 600 !important; }

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid var(--border) !important;
    gap: 0 !important;
    margin-bottom: 1rem !important;
}
.stTabs [data-baseweb="tab"] {
    font-weight: 600 !important;
    color: var(--muted) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    padding: 0.8rem 1.4rem !important;
    margin-bottom: -2px !important;
    transition: color 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    color: var(--rose) !important;
    border-bottom: 3px solid var(--rose) !important;
}

/* === INPUTS === */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--white) !important;
    color: var(--text) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    padding: 0.5rem 0.75rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--rose) !important;
    box-shadow: 0 0 0 3px rgba(196,154,108,0.15) !important;
    outline: none !important;
}
.stSelectbox > div > div[data-baseweb="select"] > div {
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--white) !important;
}
.stDateInput > div > div > input {
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--white) !important;
}

/* === FORM CONTAINER === */
[data-testid="stForm"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.5rem 1.8rem !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05) !important;
}

/* === DATAFRAME & DATA EDITOR === */
[data-testid="stDataFrame"],
[data-testid="stDataEditor"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 18px rgba(0,0,0,0.07) !important;
    border: 1px solid var(--border) !important;
}

/* === ALERTS === */
[data-testid="stAlert"] { border-radius: 12px !important; }
div[data-baseweb="notification"] { border-radius: 12px !important; }

/* === DIVIDER === */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* === SPINNER === */
[data-testid="stSpinner"] > div { border-top-color: var(--rose) !important; }

/* === SLIDER === */
[data-testid="stSlider"] > div > div > div { background: var(--rose) !important; }
[data-testid="stSlider"] [role="slider"] { background: var(--rose-dark) !important; border-color: var(--rose) !important; }
</style>
""")


# =====================================================================
# 👩‍💼 EMPLEADAS Y CONFIGURACIÓN
# =====================================================================
LISTA_EMPLEADAS = [
    "Seleccione una empleada...",
    "Francis Mendoza",
    "Wendy Millan",
    "Arlines Sagredo",
    "Sylvia Catalan",
    "Irene Millan",
    "Jhoanna Martinez",
    "Aracelis Ostos",
    "Karime Alvarez",
    "Anny Rivas"
]


# =====================================================================
# 🗄️ BASE DE DATOS — POSTGRESQL (SUPABASE)
# =====================================================================
@st.cache_resource
def get_engine():
    """
    Conecta a PostgreSQL usando psycopg3 (compatible con Python 3.12+).
    Supabase recomienda el puerto 6543 (Transaction Pooler) para apps web.
    """
    if "DATABASE_URL" not in st.secrets:
        st.error("❌ Falta la variable DATABASE_URL en los Secrets de Streamlit.")
        st.info("Ve a **Manage app → Secrets** y agrega tu URL de Supabase.")
        st.stop()

    raw_url = st.secrets["DATABASE_URL"]

    # Normalizar prefijo para psycopg3 con SQLAlchemy
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw_url.startswith("postgresql://") and "+psycopg" not in raw_url:
        raw_url = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)

    try:
        eng = create_engine(
            raw_url,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=5,
            max_overflow=3,
            connect_args={"sslmode": "require"},
        )
        # Verificar que la conexión funciona al arrancar
        with eng.connect() as test_conn:
            test_conn.execute(text("SELECT 1"))
        return eng
    except Exception as e:
        st.error("❌ No se pudo conectar a la base de datos.")
        st.markdown("""
**Verifica lo siguiente en los Secrets de Streamlit:**

1. La URL debe ser la del **Transaction Pooler** (puerto **6543**):