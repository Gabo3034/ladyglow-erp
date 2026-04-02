import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import re
import io
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="LadyGlow ERP", layout="wide", page_icon="✦")

# =====================================================================
# 🎨 TEMA VISUAL — ROSE GOLD · MAUVE · CREAM
# =====================================================================
st.markdown("""
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
""", unsafe_allow_html=True)


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
    """Conecta a PostgreSQL con pool de conexiones y reconexión automática."""
    return create_engine(
        st.secrets["DATABASE_URL"],
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=5,
        max_overflow=3
    )

engine = get_engine()


def exec_sql(query: str, params: dict = None):
    """Ejecuta INSERT / UPDATE / DELETE en una transacción."""
    with engine.begin() as conn:
        conn.execute(text(query), params or {})


def exec_many(query: str, params_list: list):
    """Ejecuta la misma query para múltiples filas (equivalente a executemany)."""
    if not params_list:
        return
    with engine.begin() as conn:
        conn.execute(text(query), params_list)


def fetch_one(query: str, params: dict = None):
    """Retorna la primera fila de una consulta SELECT."""
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchone()


def read_df(query: str, params: dict = None) -> pd.DataFrame:
    """Retorna un DataFrame desde una consulta SELECT."""
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        rows = result.fetchall()
        cols = list(result.keys())
        return pd.DataFrame(rows, columns=cols)


# =====================================================================
# 🏗️ CREACIÓN DE TABLAS
# =====================================================================
_DDL = """
CREATE TABLE IF NOT EXISTS caja_chica (
    id SERIAL PRIMARY KEY,
    fecha TEXT,
    detalle TEXT,
    tipo_movimiento TEXT,
    empleado TEXT,
    ingreso REAL,
    egreso REAL,
    registrado_por TEXT,
    forma_pago TEXT DEFAULT 'Efectivo'
);
CREATE TABLE IF NOT EXISTS prestamos (
    id SERIAL PRIMARY KEY,
    fecha TEXT,
    empleado TEXT,
    monto_total REAL,
    valor_cuota REAL,
    estado TEXT DEFAULT 'Activo'
);
CREATE TABLE IF NOT EXISTS pagos_prestamo (
    id SERIAL PRIMARY KEY,
    prestamo_id INTEGER,
    mes TEXT,
    monto REAL
);
CREATE TABLE IF NOT EXISTS gastos_admin (
    id SERIAL PRIMARY KEY,
    mes TEXT,
    fecha TEXT,
    descripcion TEXT,
    tipo TEXT,
    forma_pago TEXT DEFAULT 'Transferencia',
    empleado TEXT,
    monto REAL
);
CREATE TABLE IF NOT EXISTS sueldos_base (
    id SERIAL PRIMARY KEY,
    mes TEXT,
    empleado TEXT,
    monto REAL
);
"""

# Migraciones seguras (añadir columnas si no existen)
_MIGRATIONS = [
    "ALTER TABLE caja_chica ADD COLUMN IF NOT EXISTS forma_pago TEXT DEFAULT 'Efectivo'",
    "ALTER TABLE gastos_admin ADD COLUMN IF NOT EXISTS fecha TEXT",
    "ALTER TABLE gastos_admin ADD COLUMN IF NOT EXISTS empleado TEXT",
    "ALTER TABLE gastos_admin ADD COLUMN IF NOT EXISTS forma_pago TEXT DEFAULT 'Transferencia'",
]

with engine.begin() as _conn:
    for _stmt in _DDL.strip().split(";"):
        _stmt = _stmt.strip()
        if _stmt:
            _conn.execute(text(_stmt))
    for _mig in _MIGRATIONS:
        try:
            _conn.execute(text(_mig))
        except Exception:
            pass


# =====================================================================
# 🔐 SISTEMA DE LOGIN
# =====================================================================
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = None
    st.session_state['rol'] = None


def login():
    # Encabezado de marca
    st.markdown("""
    <div style="display:flex; justify-content:center; padding: 4rem 0 1.5rem;">
        <div style="text-align:center; max-width:420px; width:100%;">
            <div style="
                width:72px; height:72px; border-radius:50%;
                background: linear-gradient(135deg, #C49A6C, #9B7EA6);
                display:flex; align-items:center; justify-content:center;
                margin: 0 auto 1rem; font-size:1.8rem; color:white;
                box-shadow: 0 8px 28px rgba(196,154,108,0.45);
            ">✦</div>
            <div style="font-family:'DM Serif Display',serif; font-size:2.6rem; color:#2D2020; margin:0; line-height:1;">LadyGlow</div>
            <div style="font-family:'Nunito',sans-serif; font-size:0.72rem; color:#9B7EA6; letter-spacing:3.5px; text-transform:uppercase; margin-top:0.4rem;">Sistema de Gestión</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("""
        <div style="
            background: white; border: 1px solid #E2D0C0; border-radius: 20px;
            padding: 2rem 2rem 1.5rem; box-shadow: 0 8px 40px rgba(0,0,0,0.09);
        ">
        <p style="text-align:center; color:#9A8A8A; font-size:0.85rem; margin-bottom:1rem; font-weight:600;">Ingresa tus credenciales</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            user = st.text_input("👤  Usuario")
            password = st.text_input("🔑  Contraseña", type="password")
            submit = st.form_submit_button("Ingresar al Sistema", use_container_width=True)

            if submit:
                if user.lower() == "admin" and password == "1234":
                    st.session_state['usuario'] = "Admin"
                    st.session_state['rol'] = "admin"
                    st.rerun()
                elif user.lower() == "anny" and password == "anny123":
                    st.session_state['usuario'] = "Anny"
                    st.session_state['rol'] = "caja"
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")


def logout():
    st.session_state['usuario'] = None
    st.session_state['rol'] = None
    st.rerun()


if st.session_state['usuario'] is None:
    login()
    st.stop()


# =====================================================================
# 🎀 SIDEBAR — BRANDING + NAVEGACIÓN
# =====================================================================
st.sidebar.markdown(f"""
<div style="text-align:center; padding: 1.2rem 0 0.6rem;">
    <div style="
        width:52px; height:52px; border-radius:50%;
        background: linear-gradient(135deg, #C49A6C, #9B7EA6);
        display:flex; align-items:center; justify-content:center;
        margin: 0 auto 0.7rem; font-size:1.2rem; color:white;
        box-shadow: 0 4px 16px rgba(196,154,108,0.4);
    ">✦</div>
    <div style="font-family:'DM Serif Display',serif; font-size:1.4rem; color:#2D2020; line-height:1.1;">LadyGlow</div>
    <div style="font-family:'Nunito',sans-serif; font-size:0.65rem; color:#9B7EA6; letter-spacing:2.5px; text-transform:uppercase; margin-top:0.2rem;">ERP · Sistema</div>
</div>
<hr style="border-color:#E2D0C0; margin:0.8rem 0;">
<div style="
    background: rgba(196,154,108,0.12); border-radius:10px; padding:0.5rem 0.8rem;
    display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;
">
    <span style="font-size:1rem;">👤</span>
    <div>
        <div style="font-size:0.65rem; color:#9A8A8A; font-weight:700; text-transform:uppercase; letter-spacing:0.8px;">Conectado</div>
        <div style="font-size:0.9rem; font-weight:700; color:#2D2020;">{st.session_state['usuario']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("⬅️  Cerrar Sesión", use_container_width=True):
    logout()

st.sidebar.markdown("<hr style='border-color:#E2D0C0;'>", unsafe_allow_html=True)


# =====================================================================
# ⚙️ FUNCIONES GLOBALES
# =====================================================================
def load_bewe_csv(uploaded_file):
    """Carga y limpia un CSV exportado de Bewe. Normaliza columnas a minúsculas."""
    try:
        content = uploaded_file.getvalue().decode('utf-8-sig')
    except UnicodeDecodeError:
        content = uploaded_file.getvalue().decode('latin-1')

    content = content.replace('"', '')
    df = pd.read_csv(io.StringIO(content), sep=';', dtype=str)

    # Limpieza de nombres de columna + normalización a minúsculas para PostgreSQL
    df.columns = [
        str(col).replace('\ufeff', '').replace('ï»¿', '').strip().lower()
        for col in df.columns
    ]

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df.loc[df[col].isin(['nan', 'None', '']), col] = pd.NA

    return df


def clean_currency(val):
    if pd.isna(val) or val == '':
        return 0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(' ', '').replace('$', '')
    if ',' in s and '.' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        s = s.replace(',', '.')
    elif '.' in s:
        if re.search(r'\.\d{3}$', s):
            s = s.replace('.', '')
    return pd.to_numeric(s, errors='coerce')


def format_clp(val):
    try:
        return f"${int(val):,.0f}".replace(',', '.')
    except Exception:
        return "$0"


def parse_spanish_date(date_series):
    months = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

    def convert_date(d):
        if pd.isna(d):
            return None
        try:
            s = str(d).lower()
            found_month = next((m for m in months if m in s), None)
            if not found_month:
                return None
            year = re.search(r'\d{4}', s).group(0) if re.search(r'\d{4}', s) else '2026'
            day_match = re.search(r'(\d{1,2})\s*(?:de\s*)?' + found_month, s)
            day = day_match.group(1).zfill(2) if day_match else '01'
            return f"{year}-{months[found_month]}-{day}"
        except Exception:
            return None

    return pd.to_datetime(date_series.apply(convert_date), errors='coerce')


# =====================================================================
# 📓 MÓDULO ANNY — CAJA CHICA Y RENDICIONES
# =====================================================================
if st.session_state['rol'] == 'caja':
    st.markdown("# 📓 Libro de Caja Chica")
    st.markdown("Registra y revisa todos los movimientos de caja del mes.")
    st.markdown("---")

    col_form, col_tabla = st.columns([1, 2])

    with col_form:
        st.markdown("### Nuevo Movimiento")
        with st.form("registro_caja"):
            fecha = st.date_input("Fecha", datetime.today())
            detalle = st.text_input("Detalle", placeholder="Ej. Insumos limpieza, Adelanto semana")
            tipo = st.selectbox("Clasificación", [
                "Fondo de Caja (Ingreso)", "Gasto Fijo", "Gasto Variable",
                "Adelanto a Personal", "Préstamo a Personal", "Entrega Efectivo a Jefatura"
            ])
            forma_pago = st.selectbox("Medio de Pago", ["Efectivo", "Transferencia", "Tarjeta"])
            empleado_adelanto = st.selectbox(
                "Empleada (obligatorio para Adelantos / Préstamos)", LISTA_EMPLEADAS
            )
            monto = st.number_input("Monto ($)", min_value=0.0, step=1000.0)
            submit_caja = st.form_submit_button("💾 Guardar Registro", use_container_width=True)

            if submit_caja:
                necesita_empleado = "Adelanto" in tipo or "Préstamo" in tipo or "Jefatura" in tipo
                if necesita_empleado and empleado_adelanto == "Seleccione una empleada...":
                    st.error("⚠️ Debes seleccionar el nombre de la empleada.")
                else:
                    ingreso = monto if "Ingreso" in tipo else 0.0
                    egreso  = monto if "Ingreso" not in tipo else 0.0
                    tipo_db = tipo.split(' (')[0]
                    empleado_final = empleado_adelanto if necesita_empleado else ""
                    fecha_str = fecha.strftime("%Y-%m-%d")

                    existing = fetch_one(
                        "SELECT id FROM caja_chica WHERE fecha=:f AND detalle=:d AND ingreso=:i AND egreso=:e",
                        {"f": fecha_str, "d": detalle, "i": ingreso, "e": egreso}
                    )
                    if existing:
                        st.error("🛑 Registro duplicado. Cambia el detalle si es un gasto distinto.")
                    else:
                        exec_sql(
                            """INSERT INTO caja_chica
                               (fecha, detalle, tipo_movimiento, empleado, ingreso, egreso, registrado_por, forma_pago)
                               VALUES (:f, :d, :t, :e, :i, :eg, :r, :fp)""",
                            {"f": fecha_str, "d": detalle, "t": tipo_db, "e": empleado_final,
                             "i": ingreso, "eg": egreso, "r": st.session_state['usuario'], "fp": forma_pago}
                        )
                        st.success("✅ Guardado correctamente")
                        st.rerun()

    with col_tabla:
        st.markdown("### Resumen y Edición de Movimientos")
        df_caja_all = read_df("SELECT * FROM caja_chica ORDER BY fecha DESC")

        if not df_caja_all.empty:
            df_caja_all['Mes'] = pd.to_datetime(df_caja_all['fecha']).dt.strftime('%Y-%m')
            mes_caja_sel = st.selectbox("Filtrar por Mes:", sorted(df_caja_all['Mes'].unique(), reverse=True))

            df_mes = df_caja_all[df_caja_all['Mes'] == mes_caja_sel].copy()
            df_mes['fecha'] = pd.to_datetime(df_mes['fecha']).dt.date

            st.markdown("**💰 Flujo de Efectivo Físico por Semana**")
            df_efectivo = df_mes[df_mes['forma_pago'] == 'Efectivo'].copy()
            if not df_efectivo.empty:
                df_efectivo['Semana'] = pd.to_datetime(df_efectivo['fecha']).dt.day.apply(
                    lambda x: f"Semana {((x-1)//7)+1}"
                )
                resumen_sem = df_efectivo.groupby('Semana').agg(
                    Ingreso_Efectivo=('ingreso', 'sum'),
                    Egreso_Efectivo=('egreso', 'sum')
                ).reset_index()
                resumen_sem['Saldo Final (Efectivo)'] = resumen_sem['Ingreso_Efectivo'] - resumen_sem['Egreso_Efectivo']

                st.dataframe(
                    resumen_sem.style.format({
                        "Ingreso_Efectivo": format_clp,
                        "Egreso_Efectivo": format_clp,
                        "Saldo Final (Efectivo)": format_clp
                    }),
                    use_container_width=True, hide_index=True
                )
                saldo_mes = resumen_sem['Ingreso_Efectivo'].sum() - resumen_sem['Egreso_Efectivo'].sum()
                st.info(
                    f"📊 **SALDO MES EFECTIVO:** "
                    f"Ingresó: **{format_clp(resumen_sem['Ingreso_Efectivo'].sum())}** | "
                    f"Salió: **{format_clp(resumen_sem['Egreso_Efectivo'].sum())}** | "
                    f"En Caja: **{format_clp(saldo_mes)}**"
                )
            else:
                st.warning("No hay movimientos en efectivo para este mes.")

            st.markdown("---")
            st.markdown("✏️ **Edita o elimina registros:** *(selecciona una fila y presiona 'Suprimir' para borrarla)*")

            edited_caja = st.data_editor(
                df_mes[['id', 'fecha', 'detalle', 'tipo_movimiento', 'forma_pago', 'empleado', 'ingreso', 'egreso']],
                num_rows="dynamic",
                column_config={
                    "id": None,
                    "fecha": st.column_config.DateColumn("Fecha"),
                    "detalle": st.column_config.TextColumn("Detalle"),
                    "tipo_movimiento": st.column_config.SelectboxColumn("Tipo", options=[
                        "Fondo de Caja", "Gasto Fijo", "Gasto Variable",
                        "Adelanto a Personal", "Préstamo a Personal", "Entrega Efectivo a Jefatura"
                    ]),
                    "forma_pago": st.column_config.SelectboxColumn("Pago", options=["Efectivo", "Transferencia", "Tarjeta"]),
                    "empleado": st.column_config.SelectboxColumn("Empleado", options=LISTA_EMPLEADAS),
                    "ingreso": st.column_config.NumberColumn("Ingreso ($)", min_value=0),
                    "egreso": st.column_config.NumberColumn("Egreso ($)", min_value=0)
                },
                use_container_width=True, hide_index=True, key=f"edit_caja_{mes_caja_sel}"
            )

            if st.button("💾 Guardar Cambios de la Tabla", type="primary"):
                ids_to_delete = df_mes['id'].dropna().tolist()
                with engine.begin() as _c:
                    if ids_to_delete:
                        _c.execute(text("DELETE FROM caja_chica WHERE id=:id"),
                                   [{"id": i} for i in ids_to_delete])
                    for _, row in edited_caja.iterrows():
                        f_val = str(row['fecha'])[:10] if pd.notna(row['fecha']) else datetime.today().strftime("%Y-%m-%d")
                        emp_val = row['empleado'] if pd.notna(row['empleado']) else ""
                        _c.execute(
                            text("""INSERT INTO caja_chica
                                    (fecha, detalle, tipo_movimiento, empleado, ingreso, egreso, registrado_por, forma_pago)
                                    VALUES (:f, :d, :t, :e, :i, :eg, :r, :fp)"""),
                            {"f": f_val, "d": row['detalle'], "t": row['tipo_movimiento'],
                             "e": emp_val, "i": row.get('ingreso', 0), "eg": row.get('egreso', 0),
                             "r": st.session_state['usuario'], "fp": row['forma_pago']}
                        )
                st.success("✅ Cambios guardados correctamente.")
                st.rerun()
        else:
            st.info("No hay movimientos registrados en el sistema aún.")


# =====================================================================
# 📊 MÓDULO ADMIN — SISTEMA CENTRAL
# =====================================================================
elif st.session_state['rol'] == 'admin':
    st.markdown("# 📊 Sistema Central LadyGlow")
    st.markdown("---")

    tab_dash, tab_gastos, tab_prestamos, tab_import = st.tabs([
        "📊 Dashboard y Nómina",
        "💳 Gastos Operativos",
        "💸 Préstamos",
        "📂 Importar Datos"
    ])

    # ------------------------------------------------------------------
    # 📂 PESTAÑA: IMPORTADOR
    # ------------------------------------------------------------------
    with tab_import:
        st.markdown("### Carga Mensual de Archivos Bewe")
        st.markdown("Sube los dos exportes del mes para actualizar la base de datos.")
        st.markdown("")

        col1, col2 = st.columns(2)
        with col1:
            file_facturacion = st.file_uploader("1️⃣ Facturación (Tickets de Bewe)", type="csv")
        with col2:
            file_comisiones = st.file_uploader("2️⃣ Comisiones (Detalle de Bewe)", type="csv")

        if file_facturacion and file_comisiones:
            if st.button("💾 Procesar y Guardar en Base de Datos", type="primary"):
                with st.spinner('Procesando datos...'):
                    # Facturación
                    df_v = load_bewe_csv(file_facturacion)
                    # Detectar columna de fecha (nombre normalizado a minúsculas)
                    fecha_col_v = next((c for c in df_v.columns if 'fecha' in c), None)
                    if fecha_col_v:
                        df_v['fecha'] = parse_spanish_date(df_v[fecha_col_v])
                    df_v['mes'] = df_v['fecha'].dt.strftime('%Y-%m')
                    if 'empleado' in df_v.columns:
                        df_v['empleado'] = df_v['empleado'].astype(str).str.strip()

                    # Comisiones
                    df_c = load_bewe_csv(file_comisiones)
                    fecha_col_c = next((c for c in df_c.columns if 'fecha' in c), None)
                    if fecha_col_c:
                        df_c['fecha_dt'] = parse_spanish_date(df_c[fecha_col_c])
                        df_c['mes'] = df_c['fecha_dt'].dt.strftime('%Y-%m')
                    if 'mes' in df_c.columns:
                        mode_mes = df_c['mes'].mode()
                        df_c['mes'] = df_c['mes'].fillna(mode_mes[0] if not mode_mes.empty else None)

                    comision_col = next((c for c in df_c.columns if c.startswith('comis') and 'num' not in c), None)
                    if comision_col:
                        df_c['comision_num'] = df_c[comision_col].apply(clean_currency)
                    cobrado_col = next((c for c in df_c.columns if c.startswith('cobrado') and 'num' not in c), None)
                    if cobrado_col:
                        df_c['cobrado_num'] = df_c[cobrado_col].apply(clean_currency)

                    # Detectar Beneficiario Real
                    df_c['beneficiario_real'] = None
                    empleado_actual_titulo = None
                    cliente_col = next((c for c in df_c.columns if 'cliente' in c), None)
                    servicio_col = next((c for c in df_c.columns if 'servicio' in c), None)
                    empleado_col_c = next((c for c in df_c.columns if c == 'empleado'), None)

                    for idx, row in df_c.iterrows():
                        if (cliente_col and pd.notna(row.get(cliente_col)) and
                                (not servicio_col or pd.isna(row.get(servicio_col))) and
                                (not empleado_col_c or pd.isna(row.get(empleado_col_c)))):
                            empleado_actual_titulo = str(row[cliente_col]).strip()
                        elif 'comision_num' in df_c.columns and pd.notna(row.get('comision_num')) and row.get('comision_num', 0) > 0:
                            df_c.at[idx, 'beneficiario_real'] = empleado_actual_titulo

                    df_c['beneficiario_real'] = df_c['beneficiario_real'].astype(str).apply(
                        lambda x: re.split(r'[\r\n]+', x)[0].strip()
                    )

                    # Borrar datos existentes del período y reinsertar
                    meses_detectados = list(set(df_v['mes'].dropna()) | set(df_c['mes'].dropna()))
                    with engine.begin() as _c:
                        for mes in meses_detectados:
                            try:
                                _c.execute(text("DELETE FROM db_facturacion WHERE mes = :m"), {"m": mes})
                                _c.execute(text("DELETE FROM db_comisiones WHERE mes = :m"), {"m": mes})
                            except Exception:
                                pass

                    df_v.to_sql('db_facturacion', engine, if_exists='append', index=False)
                    df_c.to_sql('db_comisiones', engine, if_exists='append', index=False)
                    st.success("✅ Datos guardados correctamente en la base de datos.")

    # ------------------------------------------------------------------
    # 💳 PESTAÑA: GASTOS OPERATIVOS
    # ------------------------------------------------------------------
    with tab_gastos:
        st.markdown("### Gestión de Gastos Operativos y Adelantos")
        col_g1, col_g2 = st.columns([1, 2])

        with col_g1:
            st.markdown("#### Nuevo Gasto / Adelanto")
            with st.form("admin_gasto_form"):
                fecha_a = st.date_input("Fecha")
                detalle_a = st.text_input("Detalle", placeholder="Ej. Arriendo, Adelanto Juanita")
                tipo_a = st.selectbox("Tipo", ["Fijo", "Variable", "Adelanto a Personal"])
                forma_a = st.selectbox("Forma de Pago", ["Transferencia", "Efectivo", "Tarjeta"])
                emp_a = st.selectbox("Empleada (obligatorio si es Adelanto)", LISTA_EMPLEADAS)
                monto_a = st.number_input("Monto ($)", min_value=0.0, step=1000.0)

                if st.form_submit_button("Registrar Movimiento", use_container_width=True):
                    if tipo_a == "Adelanto a Personal" and emp_a == "Seleccione una empleada...":
                        st.error("⚠️ Debes seleccionar una empleada para un Adelanto.")
                    elif monto_a <= 0:
                        st.error("⚠️ El monto debe ser mayor a cero.")
                    else:
                        mes_a = fecha_a.strftime("%Y-%m")
                        fecha_str = fecha_a.strftime("%Y-%m-%d")
                        existing = fetch_one(
                            "SELECT id FROM gastos_admin WHERE fecha=:f AND descripcion=:d AND monto=:m",
                            {"f": fecha_str, "d": detalle_a, "m": monto_a}
                        )
                        if existing:
                            st.error("🛑 Gasto duplicado. Cambia el detalle si es un pago nuevo.")
                        else:
                            exec_sql(
                                """INSERT INTO gastos_admin (mes, fecha, descripcion, tipo, forma_pago, empleado, monto)
                                   VALUES (:mes, :f, :d, :t, :fp, :e, :m)""",
                                {"mes": mes_a, "f": fecha_str, "d": detalle_a, "t": tipo_a,
                                 "fp": forma_a, "e": emp_a if tipo_a == "Adelanto a Personal" else "", "m": monto_a}
                            )
                            st.success("✅ Guardado correctamente")
                            st.rerun()

        with col_g2:
            st.markdown("#### Revisión y Edición Mensual")
            try:
                meses_db_g_df = read_df(
                    "SELECT DISTINCT mes FROM gastos_admin "
                    "UNION SELECT DISTINCT mes FROM db_facturacion"
                )
                meses_disp_g = sorted(meses_db_g_df.iloc[:, 0].dropna().tolist(), reverse=True)
            except Exception:
                meses_disp_g = []

            if not meses_disp_g:
                st.info("No hay datos históricos registrados aún.")
            else:
                mes_g_sel = st.selectbox("Selecciona el mes:", meses_disp_g)
                df_gastos_admin = read_df(
                    "SELECT id, fecha, descripcion, tipo, forma_pago, empleado, monto FROM gastos_admin WHERE mes=:mes",
                    {"mes": mes_g_sel}
                )
                df_gastos_admin['fecha'] = pd.to_datetime(
                    df_gastos_admin['fecha'].fillna(mes_g_sel + '-01')
                ).dt.date
                df_gastos_admin['forma_pago'] = df_gastos_admin['forma_pago'].fillna('Transferencia')
                df_gastos_admin['empleado'] = df_gastos_admin['empleado'].fillna('')

                st.markdown("✏️ **Edita o elimina filas:**")
                edited_gastos = st.data_editor(
                    df_gastos_admin,
                    num_rows="dynamic",
                    key=f"editor_gastos_admin_{mes_g_sel}",
                    column_config={
                        "id": None,
                        "fecha": st.column_config.DateColumn("Fecha"),
                        "descripcion": st.column_config.TextColumn("Detalle", required=True),
                        "tipo": st.column_config.SelectboxColumn("Tipo", options=["Fijo", "Variable", "Adelanto a Personal"], required=True),
                        "forma_pago": st.column_config.SelectboxColumn("Pago", options=["Transferencia", "Efectivo", "Tarjeta"], required=True),
                        "empleado": st.column_config.SelectboxColumn("Empleado", options=LISTA_EMPLEADAS),
                        "monto": st.column_config.NumberColumn("Monto ($)", min_value=0, step=1000)
                    },
                    use_container_width=True, hide_index=True
                )

                if st.button("💾 Guardar Cambios del Mes", type="primary"):
                    ids_to_delete = df_gastos_admin['id'].dropna().tolist()
                    with engine.begin() as _c:
                        if ids_to_delete:
                            _c.execute(text("DELETE FROM gastos_admin WHERE id=:id"),
                                       [{"id": i} for i in ids_to_delete])
                        for _, row in edited_gastos.iterrows():
                            if pd.notna(row['descripcion']) and str(row['descripcion']).strip() != "" and row['monto'] > 0:
                                f_val = str(row['fecha'])[:10] if pd.notna(row['fecha']) else datetime.today().strftime("%Y-%m-%d")
                                emp_val = row['empleado'] if pd.notna(row['empleado']) else ""
                                _c.execute(
                                    text("""INSERT INTO gastos_admin (mes, fecha, descripcion, tipo, forma_pago, empleado, monto)
                                            VALUES (:mes, :f, :d, :t, :fp, :e, :m)"""),
                                    {"mes": mes_g_sel, "f": f_val, "d": str(row['descripcion']).strip(),
                                     "t": row['tipo'], "fp": row['forma_pago'], "e": emp_val, "m": row['monto']}
                                )
                    st.success(f"✅ Gastos de {mes_g_sel} actualizados correctamente.")
                    st.rerun()

    # ------------------------------------------------------------------
    # 💸 PESTAÑA: PRÉSTAMOS
    # ------------------------------------------------------------------
    with tab_prestamos:
        st.markdown("### Gestión de Préstamos al Equipo")
        col_p1, col_p2 = st.columns([1, 2])

        with col_p1:
            st.markdown("#### Nuevo Préstamo")
            with st.form("form_prestamo"):
                emp_prestamo = st.selectbox("Empleada que recibe el préstamo", LISTA_EMPLEADAS)
                monto_total = st.number_input("Monto Total Prestado ($)", min_value=0, step=10000)
                valor_cuota = st.number_input("¿Cuánto descontar por mes? ($)", min_value=0, step=5000)
                fecha_p = st.date_input("Fecha de Aprobación")

                if st.form_submit_button("Crear Préstamo", use_container_width=True):
                    if emp_prestamo == "Seleccione una empleada...":
                        st.error("Seleccione a la empleada.")
                    elif monto_total <= 0 or valor_cuota <= 0:
                        st.error("El monto y la cuota deben ser mayores a cero.")
                    else:
                        exec_sql(
                            "INSERT INTO prestamos (fecha, empleado, monto_total, valor_cuota) VALUES (:f, :e, :m, :v)",
                            {"f": fecha_p.strftime("%Y-%m-%d"), "e": emp_prestamo, "m": monto_total, "v": valor_cuota}
                        )
                        st.success("✅ Préstamo registrado correctamente.")
                        st.rerun()

        with col_p2:
            st.markdown("#### Estado de Préstamos")
            st.markdown("✏️ **Edita o elimina préstamos:**")
            df_prestamos = read_df("SELECT * FROM prestamos")

            if not df_prestamos.empty:
                resumen_prestamos = []
                for _, row in df_prestamos.iterrows():
                    p_id = row['id']
                    df_pagos = read_df(
                        "SELECT COALESCE(SUM(monto), 0) as total FROM pagos_prestamo WHERE prestamo_id=:pid",
                        {"pid": p_id}
                    )
                    total_pagado = df_pagos.iloc[0]['total'] if not df_pagos.empty else 0
                    saldo = row['monto_total'] - total_pagado
                    resumen_prestamos.append({
                        "id": p_id, "fecha": row['fecha'], "empleado": row['empleado'],
                        "monto_total": row['monto_total'], "valor_cuota": row['valor_cuota'],
                        "Abonado": total_pagado, "Saldo Deuda": saldo, "estado": row['estado']
                    })

                df_resumen_p = pd.DataFrame(resumen_prestamos)
                df_resumen_p['fecha'] = pd.to_datetime(df_resumen_p['fecha']).dt.date

                edited_prestamos = st.data_editor(
                    df_resumen_p,
                    num_rows="dynamic",
                    key="editor_prestamos_admin",
                    disabled=["Abonado", "Saldo Deuda", "id"],
                    column_config={
                        "id": None,
                        "fecha": st.column_config.DateColumn("Fecha"),
                        "empleado": st.column_config.SelectboxColumn("Empleado", options=LISTA_EMPLEADAS),
                        "monto_total": st.column_config.NumberColumn("Monto Total ($)", min_value=0, step=10000),
                        "valor_cuota": st.column_config.NumberColumn("Cuota Mensual ($)", min_value=0, step=5000),
                        "Abonado": st.column_config.NumberColumn("Abonado ($)", format="$ %d"),
                        "Saldo Deuda": st.column_config.NumberColumn("Saldo Deuda ($)", format="$ %d"),
                        "estado": st.column_config.SelectboxColumn("Estado", options=["Activo", "Pagado", "Cancelado"])
                    },
                    use_container_width=True, hide_index=True
                )

                if st.button("💾 Guardar Cambios de Préstamos", type="primary"):
                    ids_originales = df_resumen_p['id'].tolist()
                    ids_nuevos = edited_prestamos['id'].dropna().tolist()
                    ids_eliminados = list(set(ids_originales) - set(ids_nuevos))

                    with engine.begin() as _c:
                        if ids_eliminados:
                            _c.execute(text("DELETE FROM prestamos WHERE id=:id"),
                                       [{"id": i} for i in ids_eliminados])
                            _c.execute(text("DELETE FROM pagos_prestamo WHERE prestamo_id=:id"),
                                       [{"id": i} for i in ids_eliminados])

                        for _, row in edited_prestamos.iterrows():
                            f_val = str(row['fecha'])[:10] if pd.notna(row['fecha']) else datetime.today().strftime("%Y-%m-%d")
                            if pd.notna(row['id']):
                                _c.execute(
                                    text("UPDATE prestamos SET fecha=:f, empleado=:e, monto_total=:m, valor_cuota=:v, estado=:s WHERE id=:id"),
                                    {"f": f_val, "e": row['empleado'], "m": row['monto_total'],
                                     "v": row['valor_cuota'], "s": row['estado'], "id": row['id']}
                                )
                            else:
                                _c.execute(
                                    text("INSERT INTO prestamos (fecha, empleado, monto_total, valor_cuota, estado) VALUES (:f, :e, :m, :v, :s)"),
                                    {"f": f_val, "e": row['empleado'], "m": row['monto_total'],
                                     "v": row['valor_cuota'], "s": row['estado']}
                                )

                    st.success("✅ Cambios en préstamos guardados correctamente.")
                    st.rerun()
            else:
                st.info("No hay préstamos registrados.")

    # ------------------------------------------------------------------
    # 📊 PESTAÑA: DASHBOARD Y NÓMINA
    # ------------------------------------------------------------------
    with tab_dash:
        try:
            meses_df = read_df(
                "SELECT DISTINCT mes FROM db_facturacion "
                "UNION SELECT DISTINCT mes FROM db_comisiones"
            )
            meses_disponibles = sorted(meses_df.iloc[:, 0].dropna().tolist(), reverse=True)
        except Exception:
            meses_disponibles = []

        if not meses_disponibles:
            st.info("👋 Sube los archivos en la pestaña **Importar Datos** para comenzar.")
        else:
            pct_especial = st.sidebar.slider("% Comisión Francis y Wendy", 0, 100, 50) / 100
            mes_sel = st.sidebar.selectbox("Mes a Analizar:", meses_disponibles)

            # Cargar datos del mes seleccionado
            df_v_filt = read_df("SELECT * FROM db_facturacion WHERE mes = :mes", {"mes": mes_sel})
            df_c_filt = read_df("SELECT * FROM db_comisiones WHERE mes = :mes", {"mes": mes_sel})

            # --- LIMPIEZA DE INGRESOS ---
            columnas_dinero = ['total', 'deja a deber', 'saldo usado', 'en efectivo',
                               'transferencia', 'red compra', 'tarjeta de crédito', 'ingreso real']
            for col in columnas_dinero:
                if col in df_v_filt.columns:
                    df_v_filt[col] = df_v_filt[col].apply(clean_currency)
                else:
                    df_v_filt[col] = 0

            df_v_filt['ingreso real'] = (
                df_v_filt['total'] - df_v_filt['deja a deber'] - df_v_filt['saldo usado']
            )
            fpago_col = next((c for c in df_v_filt.columns if 'forma' in c and 'pago' in c), None)
            if fpago_col:
                df_v_filt.loc[
                    df_v_filt[fpago_col].str.contains('saldo|debt', case=False, na=False),
                    'ingreso real'
                ] = 0
            df_v_filt['ingreso real'] = df_v_filt['ingreso real'].clip(lower=0)

            for m in ['en efectivo', 'transferencia', 'red compra', 'tarjeta de crédito']:
                df_v_filt[f'real_{m}'] = df_v_filt.apply(
                    lambda r: r['ingreso real'] if fpago_col and str(r.get(fpago_col, '')).strip() == m
                    else (r[m] if fpago_col and str(r.get(fpago_col, '')).strip() == 'Mixto' else 0),
                    axis=1
                )

            ingreso_real_caja = df_v_filt['ingreso real'].sum()

            # --- GASTOS Y ADELANTOS ---
            df_g_db = read_df("SELECT * FROM caja_chica ORDER BY fecha")
            df_g_db['Mes'] = pd.to_datetime(df_g_db['fecha']).dt.strftime('%Y-%m')
            df_g_filt = df_g_db[df_g_db['Mes'] == mes_sel]

            df_g_admin = read_df("SELECT * FROM gastos_admin WHERE mes=:mes", {"mes": mes_sel})

            fijo_anny = df_g_filt[df_g_filt['tipo_movimiento'] == 'Gasto Fijo']['egreso'].sum()
            var_anny  = df_g_filt[df_g_filt['tipo_movimiento'] == 'Gasto Variable']['egreso'].sum()
            fijo_admin = df_g_admin[df_g_admin['tipo'] == 'Fijo']['monto'].sum() if not df_g_admin.empty else 0
            var_admin  = df_g_admin[df_g_admin['tipo'] == 'Variable']['monto'].sum() if not df_g_admin.empty else 0

            total_fijo    = fijo_anny + fijo_admin
            total_variable = var_anny + var_admin

            # Adelantos unificados
            df_adel_caja = df_g_filt[df_g_filt['tipo_movimiento'] == 'Adelanto a Personal'][
                ['empleado', 'egreso']
            ].rename(columns={'empleado': 'Empleado', 'egreso': 'Adelanto'})

            df_adel_admin = (
                df_g_admin[df_g_admin['tipo'] == 'Adelanto a Personal'][['empleado', 'monto']]
                .rename(columns={'empleado': 'Empleado', 'monto': 'Adelanto'})
                if not df_g_admin.empty else pd.DataFrame(columns=['Empleado', 'Adelanto'])
            )

            df_adelantos_total = pd.concat([df_adel_caja, df_adel_admin]).groupby('Empleado')['Adelanto'].sum().reset_index()
            df_adelantos_total.columns = ['Empleado', 'Adelantos Totales']

            # --- COMISIONES ---
            emp_col = next((c for c in df_v_filt.columns if c == 'empleado'), None)
            br_col  = next((c for c in df_c_filt.columns if 'beneficiario' in c), None)
            cn_col  = next((c for c in df_c_filt.columns if 'comision_num' in c or 'comisión_num' in c), None)
            cb_col  = next((c for c in df_c_filt.columns if 'cobrado_num' in c), None)
            tc_col  = next((c for c in df_c_filt.columns if 'tipo' in c and 'comis' in c), None)

            if emp_col:
                df_jefas = df_v_filt[df_v_filt[emp_col].str.contains(r'wendy|francis', case=False, na=False)]
                comis_jefas = df_jefas.groupby(emp_col)['ingreso real'].sum() * pct_especial
                comis_jefas = comis_jefas.reset_index().rename(
                    columns={'ingreso real': 'Comisiones Generadas', emp_col: 'Empleado'}
                )
            else:
                comis_jefas = pd.DataFrame(columns=['Empleado', 'Comisiones Generadas'])

            if br_col:
                df_resto = df_c_filt[~df_c_filt[br_col].str.contains(r'wendy|francis', case=False, na=False)]
            else:
                df_resto = df_c_filt.copy()

            # Cobrado / comision_num
            if cb_col:
                df_c_filt['cobrado_num_clean'] = df_c_filt[cb_col].apply(clean_currency)
            elif next((c for c in df_c_filt.columns if 'cobrado' in c), None):
                _cb = next(c for c in df_c_filt.columns if 'cobrado' in c)
                df_c_filt['cobrado_num_clean'] = df_c_filt[_cb].apply(clean_currency)
            else:
                df_c_filt['cobrado_num_clean'] = 0

            # Cargo especial Anny
            comision_olvidada_anny = 0
            if tc_col and br_col:
                mask_cargo_esp = df_c_filt[tc_col].astype(str).str.contains('Cargo especial', case=False, na=False)
                mask_no_anny = df_c_filt[br_col] != 'Anny Rivas'
                mask_anny    = df_c_filt[br_col] == 'Anny Rivas'
                cobrado_cargo_esp_chicas = df_c_filt[mask_cargo_esp & mask_no_anny]['cobrado_num_clean'].sum()
                if cn_col:
                    cargo_esp_ya_pagado_anny = df_c_filt[mask_cargo_esp & mask_anny][cn_col].apply(clean_currency).sum()
                else:
                    cargo_esp_ya_pagado_anny = 0
                comision_olvidada_anny = max(0, (cobrado_cargo_esp_chicas * 0.015) - cargo_esp_ya_pagado_anny)

            # Comisiones del resto
            if br_col and cn_col:
                comis_resto = df_resto.groupby(br_col)[cn_col].sum().reset_index().rename(
                    columns={br_col: 'Empleado', cn_col: 'Comisiones Generadas'}
                )
            else:
                comis_resto = pd.DataFrame(columns=['Empleado', 'Comisiones Generadas'])

            nomina_base = pd.concat([comis_jefas, comis_resto]).groupby('Empleado')['Comisiones Generadas'].sum().reset_index()

            if comision_olvidada_anny > 0:
                if 'Anny Rivas' in nomina_base['Empleado'].values:
                    nomina_base.loc[nomina_base['Empleado'] == 'Anny Rivas', 'Comisiones Generadas'] += comision_olvidada_anny
                else:
                    nomina_base = pd.concat([
                        nomina_base,
                        pd.DataFrame([{'Empleado': 'Anny Rivas', 'Comisiones Generadas': comision_olvidada_anny}])
                    ], ignore_index=True)

            # Filtrar fantasmas
            nomina_base = nomina_base[
                ~nomina_base['Empleado'].str.lower().isin(['none', 'nan', '', 'seleccione una empleada...'])
            ]

            # Adelantos
            nomina_base = pd.merge(nomina_base, df_adelantos_total, on='Empleado', how='left').fillna(0)

            # Sueldos base guardados
            df_sb = read_df("SELECT empleado, monto FROM sueldos_base WHERE mes=:mes", {"mes": mes_sel})
            dict_sueldos = dict(zip(df_sb['empleado'], df_sb['monto']))
            nomina_base['Sueldo Base (Fijo)'] = nomina_base['Empleado'].map(dict_sueldos).fillna(0)

            # Cuotas de préstamos
            dict_cuotas = {}
            df_prestamos_activos = read_df("SELECT * FROM prestamos WHERE estado='Activo'")
            for _, rp in df_prestamos_activos.iterrows():
                p_id = rp['id']
                emp  = rp['empleado']
                df_pag_mes = read_df(
                    "SELECT monto FROM pagos_prestamo WHERE prestamo_id=:pid AND mes=:mes",
                    {"pid": p_id, "mes": mes_sel}
                )
                if not df_pag_mes.empty:
                    dict_cuotas[emp] = dict_cuotas.get(emp, 0) + df_pag_mes.iloc[0]['monto']
                else:
                    df_pag_hist = read_df(
                        "SELECT COALESCE(SUM(monto),0) as t FROM pagos_prestamo WHERE prestamo_id=:pid",
                        {"pid": p_id}
                    )
                    pagado_historico = df_pag_hist.iloc[0]['t'] if not df_pag_hist.empty else 0
                    saldo_real = rp['monto_total'] - pagado_historico
                    if saldo_real > 0:
                        dict_cuotas[emp] = dict_cuotas.get(emp, 0) + min(rp['valor_cuota'], saldo_real)

            nomina_base['Cuota Préstamo'] = nomina_base['Empleado'].map(dict_cuotas).fillna(0)

            # Convertir a int
            for _c in ['Sueldo Base (Fijo)', 'Comisiones Generadas', 'Adelantos Totales', 'Cuota Préstamo']:
                nomina_base[_c] = nomina_base[_c].astype(int)

            # ==========================================
            # 🏦 FLUJO DE CAJA Y AUDITORÍA
            # ==========================================
            st.markdown(f"### 🏦 Flujo de Ingresos y Auditoría — {mes_sel}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("1️⃣ Total Facturado Bruto",   format_clp(df_v_filt['total'].sum()))
            c2.metric("2️⃣ Menos: Deudas",           f"- {format_clp(df_v_filt['deja a deber'].sum())}")
            c3.metric("3️⃣ Menos: Saldos",           f"- {format_clp(df_v_filt['saldo usado'].sum())}")
            c4.metric("💵 = INGRESO REAL EN CAJA",  format_clp(ingreso_real_caja))

            st.markdown("")
            st.markdown("**🔍 Cruce de Efectivo Físico:**")
            efectivo_bowe = df_v_filt.get('real_en efectivo', pd.Series([0])).sum()
            efectivo_anny = df_g_filt[
                (df_g_filt['tipo_movimiento'] == 'Fondo de Caja') & (df_g_filt['forma_pago'] == 'Efectivo')
            ]['ingreso'].sum()
            diff_efectivo = efectivo_anny - efectivo_bowe

            a1, a2, a3, a4 = st.columns(4)
            a1.metric("Efectivo Bewe",       format_clp(efectivo_bowe))
            a2.metric("Ingreso Físico Anny", format_clp(efectivo_anny))
            if diff_efectivo == 0:
                a3.metric("Diferencia", format_clp(diff_efectivo), "✅ Caja Cuadrada", delta_color="normal")
            else:
                a3.metric("Diferencia", format_clp(diff_efectivo),
                          "Sobra" if diff_efectivo > 0 else "⚠️ Falta", delta_color="inverse")
            a4.metric("Transferencias Bewe", format_clp(df_v_filt.get('real_transferencia', pd.Series([0])).sum()))

            # ==========================================
            # 📝 TABLA DE NÓMINA
            # ==========================================
            st.markdown("---")
            st.markdown(f"### 👩‍💼 Liquidación de Pagos — {mes_sel}")

            styled_nomina = nomina_base.style.format({
                "Comisiones Generadas": format_clp,
                "Adelantos Totales": format_clp
            })

            edited_nomina = st.data_editor(
                styled_nomina,
                key=f"editor_nomina_{mes_sel}",
                disabled=["Empleado", "Comisiones Generadas", "Adelantos Totales"],
                column_config={
                    "Empleado": st.column_config.TextColumn("Profesional", width="medium"),
                    "Sueldo Base (Fijo)": st.column_config.NumberColumn("Sueldo Base ✍️", min_value=0, step=10000),
                    "Cuota Préstamo": st.column_config.NumberColumn("Cuota Préstamo ✍️", min_value=0, step=5000),
                    "Adelantos Totales": st.column_config.TextColumn("Adelantos (Caja + Admin)")
                },
                use_container_width=True, hide_index=True
            )

            edited_nomina['TOTAL A TRANSFERIR'] = (
                edited_nomina['Sueldo Base (Fijo)'] +
                edited_nomina['Comisiones Generadas'] -
                edited_nomina['Adelantos Totales'] -
                edited_nomina['Cuota Préstamo']
            ).astype(int)

            total_pago_personal = (
                edited_nomina['TOTAL A TRANSFERIR'].sum() +
                edited_nomina['Adelantos Totales'].sum() +
                edited_nomina['Cuota Préstamo'].sum()
            )

            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                st.markdown("**💰 Montos Finales a Transferir:**")
                st.dataframe(
                    edited_nomina[['Empleado', 'TOTAL A TRANSFERIR']].style.format({"TOTAL A TRANSFERIR": format_clp}),
                    use_container_width=True, hide_index=True
                )

            with col_t2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.info("💡 Guarda los sueldos y cuotas para que el sistema recuerde y actualice los préstamos.")
                if st.button("💾 Confirmar y Guardar Sueldos + Cuotas", type="primary"):
                    with engine.begin() as _c:
                        for _, row in edited_nomina.iterrows():
                            emp         = row['Empleado']
                            cuota       = row['Cuota Préstamo']
                            sueldo_base = row['Sueldo Base (Fijo)']

                            # Guardar sueldo base
                            sb_exist = fetch_one(
                                "SELECT id FROM sueldos_base WHERE mes=:mes AND empleado=:emp",
                                {"mes": mes_sel, "emp": emp}
                            )
                            if sb_exist:
                                _c.execute(
                                    text("UPDATE sueldos_base SET monto=:m WHERE id=:id"),
                                    {"m": sueldo_base, "id": sb_exist[0]}
                                )
                            else:
                                _c.execute(
                                    text("INSERT INTO sueldos_base (mes, empleado, monto) VALUES (:mes, :emp, :m)"),
                                    {"mes": mes_sel, "emp": emp, "m": sueldo_base}
                                )

                            # Guardar cuota préstamo
                            if cuota > 0:
                                prest = fetch_one(
                                    "SELECT id, monto_total FROM prestamos WHERE empleado=:emp AND estado='Activo'",
                                    {"emp": emp}
                                )
                                if prest:
                                    p_id = prest[0]
                                    monto_total_p = prest[1]
                                    p_exist = fetch_one(
                                        "SELECT id FROM pagos_prestamo WHERE prestamo_id=:pid AND mes=:mes",
                                        {"pid": p_id, "mes": mes_sel}
                                    )
                                    if p_exist:
                                        _c.execute(
                                            text("UPDATE pagos_prestamo SET monto=:m WHERE id=:id"),
                                            {"m": cuota, "id": p_exist[0]}
                                        )
                                    else:
                                        _c.execute(
                                            text("INSERT INTO pagos_prestamo (prestamo_id, mes, monto) VALUES (:pid, :mes, :m)"),
                                            {"pid": p_id, "mes": mes_sel, "m": cuota}
                                        )
                                    # Verificar si el préstamo está saldado
                                    df_total_pag = read_df(
                                        "SELECT COALESCE(SUM(monto),0) as t FROM pagos_prestamo WHERE prestamo_id=:pid",
                                        {"pid": p_id}
                                    )
                                    total_pag = df_total_pag.iloc[0]['t'] if not df_total_pag.empty else 0
                                    nuevo_estado = 'Pagado' if total_pag >= monto_total_p else 'Activo'
                                    _c.execute(
                                        text("UPDATE prestamos SET estado=:s WHERE id=:id"),
                                        {"s": nuevo_estado, "id": p_id}
                                    )
                    st.success("✅ Sueldos base y cuotas guardados correctamente.")

            # ==========================================
            # 🏦 RESUMEN FINANCIERO FINAL
            # ==========================================
            st.markdown("---")
            st.markdown("### 🏦 Resumen Financiero Consolidado")

            utilidad = ingreso_real_caja - total_fijo - total_variable - total_pago_personal

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💵 Ingreso Real Total",   format_clp(ingreso_real_caja))
            c2.metric(
                "💳 Gastos Operativos",
                f"- {format_clp(total_fijo + total_variable)}",
                f"Admin: {format_clp(fijo_admin + var_admin)} | Caja: {format_clp(fijo_anny + var_anny)}"
            )
            c3.metric("👩‍💼 Costo Personal",       f"- {format_clp(total_pago_personal)}", "Sueldos + Comisiones")
            c4.metric(
                "💰 UTILIDAD LÍQUIDA",
                format_clp(utilidad),
                f"{(utilidad / ingreso_real_caja * 100):.1f}% de Margen" if ingreso_real_caja > 0 else ""
            )

            components.html("""
            <div style='text-align:center; margin-top:24px;'>
                <button onclick='window.parent.print()' style='
                    background: linear-gradient(135deg, #C49A6C, #A07845);
                    color: white; border: none; padding: 12px 28px;
                    border-radius: 10px; cursor: pointer; font-weight: 700;
                    font-size: 14px; letter-spacing: 0.3px;
                    box-shadow: 0 4px 18px rgba(196,154,108,0.4);
                    font-family: Nunito, sans-serif;
                '>🖨️ Generar Reporte PDF</button>
            </div>
            """)
