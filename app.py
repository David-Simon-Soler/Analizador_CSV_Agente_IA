import streamlit as st
import pandas as pd
import sqlite3
import os
import json
import plotly.express as px
from dotenv import load_dotenv
from src.loader import cargar_csvs, generar_schema_texto
from src.agente import consultar
from src.limpieza import limpiar_datos
from src.dashboard import (
    generar_config_dashboard, crear_grafico,
    calcular_kpis, generar_grafico_personalizado, COLORES
)

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

# --- CONFIG ---
st.set_page_config(page_title="CSV Analyst AI", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.kpi-card {
    background: linear-gradient(135deg, #0d1b2a, #1a3a5c);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    border: 1px solid rgba(79, 195, 247, 0.2);
    transition: all 0.3s ease;
    cursor: default;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #4FC3F7, #81C784);
}
.kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(79, 195, 247, 0.25);
    border-color: rgba(79, 195, 247, 0.5);
}
.kpi-icono { font-size: 1.8rem; margin-bottom: 8px; }
.kpi-valor {
    font-size: 2rem;
    font-weight: 700;
    color: #4FC3F7;
    margin: 6px 0;
    letter-spacing: -1px;
}
.kpi-nombre {
    font-size: 0.8rem;
    color: #90A4AE;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}
.kpi-desc {
    font-size: 0.75rem;
    color: #546E7A;
    margin-top: 4px;
}
.dashboard-titulo {
    font-size: 1.8rem;
    font-weight: 700;
    color: #E0E0E0;
    margin-bottom: 4px;
}
.dashboard-subtitulo {
    font-size: 0.9rem;
    color: #78909C;
    margin-bottom: 24px;
}
.seccion-titulo {
    font-size: 1rem;
    font-weight: 600;
    color: #90A4AE;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 24px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
for key, default in {
    "esquema": None, "schema_texto": None, "db_path": None,
    "historial": [], "graficos_config": [], "df_actual": None,
    "dashboard_generado": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- SIDEBAR ---
with st.sidebar:
    st.header("📂 Sube tus datos")
    archivos = st.file_uploader(
        "Sube uno o varios CSVs",
        type=["csv"],
        accept_multiple_files=True
    )

    if archivos:
        if st.button("⚡ Cargar datos", use_container_width=True):
            with st.spinner("Detectando estructura..."):
                esquema, db_path = cargar_csvs(archivos)
                schema_texto = generar_schema_texto(esquema)
                st.session_state.esquema = esquema
                st.session_state.schema_texto = schema_texto
                st.session_state.db_path = db_path
                st.session_state.historial = []
                st.session_state.graficos_config = []
                st.session_state.dashboard_generado = None
                st.success("✅ Datos cargados")

    if st.session_state.esquema:
        st.divider()
        st.markdown("**🗄️ Tablas detectadas:**")
        for tabla, info in st.session_state.esquema.items():
            st.markdown(f"📦 **{tabla}** — {info['filas']:,} filas")
            with st.expander("Ver columnas"):
                for col, tipo in info["tipos"].items():
                    st.markdown(f"- `{col}` ({tipo})")

# --- MAIN ---
st.title("📊 CSV Analyst AI")
st.caption("Sube tus CSVs, pregunta en español y construye dashboards interactivos.")

if not st.session_state.esquema:
    st.info("👈 Sube tus CSVs en el panel izquierdo para empezar.")
    st.stop()

tab1, tab2 = st.tabs(["💬 Consultas", "📈 Dashboard"])

# --- TAB 1: CONSULTAS ---
with tab1:
    pregunta = st.chat_input("Escribe tu pregunta aquí...")

    if pregunta:
        with st.spinner("Analizando..."):
            try:
                query, df_raw = consultar(
                    pregunta,
                    st.session_state.schema_texto,
                    st.session_state.db_path
                )
                columnas = list(df_raw.columns)
                filas = [tuple(row) for row in df_raw.values]
                df, reporte = limpiar_datos(columnas, filas)
                st.session_state.df_actual = df
                st.session_state.historial.append({
                    "pregunta": pregunta,
                    "query": query,
                    "df": df,
                    "reporte": reporte
                })
            except Exception as e:
                st.error(f"❌ {e}")

    for i, item in enumerate(reversed(st.session_state.historial)):
        with st.chat_message("user"):
            st.write(item["pregunta"])

        with st.chat_message("assistant"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📝 Query generada:**")
                st.code(item["query"], language="sql")

                if item["reporte"]:
                    with st.expander("🧹 Limpieza aplicada"):
                        for r in item["reporte"]:
                            st.write(r)

                st.markdown(f"**📊 Resultados ({len(item['df'])} filas):**")
                st.dataframe(item["df"].head(10), use_container_width=True)

                csv = item["df"].to_csv(index=False).encode("utf-8")
                st.download_button(
                    "💾 Descargar CSV", csv,
                    f"resultado_{i}.csv", "text/csv",
                    key=f"download_{i}"
                )

            with col2:
                cols_num = item["df"].select_dtypes(include='number').columns.tolist()
                cols_cat = item["df"].select_dtypes(include='object').columns.tolist()
                if cols_cat and cols_num:
                    fig = px.bar(
                        item["df"].head(20),
                        x=cols_cat[0], y=cols_num[0],
                        color=cols_cat[0],
                        color_discrete_sequence=["#4FC3F7","#81C784","#FFB74D","#CE93D8","#EF9A9A"],
                        template="plotly_dark",
                        text=cols_num[0]
                    )
                    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")

# --- TAB 2: DASHBOARD ---
with tab2:

    # Botón generar dashboard IA
    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        if st.button("🤖 Generar Dashboard con IA", use_container_width=True):
            with st.spinner("La IA está analizando tus datos y diseñando el dashboard..."):
                try:
                    schema_str = "\n".join([
                        f"Tabla '{t}': {', '.join(info['columnas'])}"
                        for t, info in st.session_state.esquema.items()
                    ])
                    config = generar_config_dashboard(schema_str)
                    st.session_state.dashboard_generado = config
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with col_btn2:
        if st.session_state.dashboard_generado:
            if st.button("🗑️ Limpiar", use_container_width=True):
                st.session_state.dashboard_generado = None
                st.session_state.graficos_config = []
                st.rerun()

    # Mostrar dashboard generado por IA
    if st.session_state.dashboard_generado:
        config = st.session_state.dashboard_generado
        conn = sqlite3.connect(st.session_state.db_path)

        st.markdown(f'<div class="dashboard-titulo">📊 {config.get("titulo", "Dashboard")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dashboard-subtitulo">Generado automáticamente por IA · {sum(info["filas"] for info in st.session_state.esquema.values()):,} registros analizados</div>', unsafe_allow_html=True)

        # KPIs
        st.markdown('<div class="seccion-titulo">KPIs principales</div>', unsafe_allow_html=True)
        kpi_cols = st.columns(4)

        for idx, kpi in enumerate(config.get("kpis", [])[:4]):
            try:
                df_kpi = pd.read_sql_query(kpi["query"], conn)
                valor = df_kpi.iloc[0, 0]
                if isinstance(valor, float):
                    valor_str = f"{valor:,.2f}"
                elif isinstance(valor, int):
                    valor_str = f"{valor:,}"
                else:
                    valor_str = str(valor)
            except Exception:
                valor_str = "N/A"

            with kpi_cols[idx]:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icono">{kpi.get('icono', '📊')}</div>
                    <div class="kpi-valor">{valor_str}</div>
                    <div class="kpi-nombre">{kpi.get('nombre', '')}</div>
                    <div class="kpi-desc">{kpi.get('descripcion', '')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")

        # Gráficos en grid 2x2
        st.markdown('<div class="seccion-titulo">Análisis visual</div>', unsafe_allow_html=True)
        graficos = config.get("graficos", [])

        for idx in range(0, len(graficos), 2):
            cols = st.columns(2)
            for j in range(2):
                if idx + j < len(graficos):
                    graf = graficos[idx + j]
                    with cols[j]:
                        try:
                            df_graf = pd.read_sql_query(graf["query"], conn)
                            fig = crear_grafico(df_graf, graf["tipo"], graf["titulo"])
                            if fig:
                                st.plotly_chart(fig, use_container_width=True, key=f"ia_{idx}_{j}")
                                with st.expander("ℹ️ Sobre este gráfico"):
                                    st.caption(graf.get("descripcion", ""))
                                    st.code(graf["query"], language="sql")
                        except Exception:
                            st.warning(f"No se pudo generar: {graf['titulo']}")

        conn.close()

    # Constructor manual
    st.divider()
    st.markdown('<div class="seccion-titulo">Constructor manual de gráficos</div>', unsafe_allow_html=True)

    if st.session_state.df_actual is not None:
        df_manual = st.session_state.df_actual

        with st.expander("⚙️ Configurar gráfico personalizado", expanded=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                tipo_m = st.selectbox("Tipo", ["Barras", "Línea", "Pie", "Scatter", "Área"], key="tipo_manual")
                titulo_m = st.text_input("Título", value="Mi gráfico", key="titulo_manual")
            with c2:
                col_x_m = st.selectbox("Eje X", df_manual.columns.tolist(), key="colx_manual")
                cols_num_m = df_manual.select_dtypes(include='number').columns.tolist()
                col_y_m = st.selectbox("Eje Y", cols_num_m if cols_num_m else df_manual.columns.tolist(), key="coly_manual")
            with c3:
                color_m = st.selectbox("Color", list(COLORES.keys()), key="color_manual")

            fig_manual = generar_grafico_personalizado(df_manual, tipo_m, col_x_m, col_y_m, color_m, titulo_m)
            if fig_manual:
                fig_manual.update_layout(template="plotly_dark")
                st.plotly_chart(fig_manual, use_container_width=True, key="manual_preview")

            if st.button("➕ Añadir al dashboard", use_container_width=True):
                st.session_state.graficos_config.append({
                    "df": df_manual, "tipo": tipo_m,
                    "col_x": col_x_m, "col_y": col_y_m,
                    "color": color_m, "titulo": titulo_m
                })
                st.success("✅ Gráfico añadido")

        if st.session_state.graficos_config:
            st.markdown('<div class="seccion-titulo">Gráficos añadidos</div>', unsafe_allow_html=True)
            for idx in range(0, len(st.session_state.graficos_config), 2):
                cols = st.columns(2)
                for j in range(2):
                    if idx + j < len(st.session_state.graficos_config):
                        cfg = st.session_state.graficos_config[idx + j]
                        fig = generar_grafico_personalizado(
                            cfg["df"], cfg["tipo"], cfg["col_x"],
                            cfg["col_y"], cfg["color"], cfg["titulo"]
                        )
                        if fig:
                            fig.update_layout(template="plotly_dark")
                            cols[j].plotly_chart(fig, use_container_width=True, key=f"manual_{idx}_{j}")
    else:
        st.info("💡 Haz una consulta primero para poder construir gráficos manuales.")