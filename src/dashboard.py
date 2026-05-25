import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Paleta profesional
PALETA = {
    "primario": "#4FC3F7",
    "secundario": "#81C784",
    "terciario": "#FFB74D",
    "cuaternario": "#CE93D8",
    "quinario": "#EF9A9A",
    "fondo": "rgba(0,0,0,0)",
    "texto": "#E0E0E0",
    "grid": "rgba(255,255,255,0.05)"
}

SECUENCIA_COLORES = [
    "#4FC3F7", "#81C784", "#FFB74D",
    "#CE93D8", "#EF9A9A", "#80DEEA"
]

LAYOUT_BASE = dict(
    plot_bgcolor=PALETA["fondo"],
    paper_bgcolor=PALETA["fondo"],
    font=dict(color=PALETA["texto"], family="Inter, sans-serif"),
    title_font=dict(size=15, color=PALETA["texto"]),
    margin=dict(l=20, r=20, t=50, b=40),
    legend=dict(
        bgcolor="rgba(255,255,255,0.05)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1
    ),
    xaxis=dict(
        gridcolor=PALETA["grid"],
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        gridcolor=PALETA["grid"],
        showgrid=True,
        zeroline=False
    )
)

def generar_config_dashboard(schema_str):
    prompt = f"""
Eres un experto en Business Intelligence. Analiza este esquema y devuelve SOLO un JSON válido sin markdown:

{{
  "titulo": "Nombre del dashboard",
  "kpis": [
    {{"nombre": "Nombre KPI", "query": "SELECT COUNT(*) as valor FROM tabla", "icono": "📦", "descripcion": "Descripcion breve"}},
    {{"nombre": "Nombre KPI 2", "query": "SELECT SUM(columna) as valor FROM tabla", "icono": "💰", "descripcion": "Descripcion breve"}}
  ],
  "graficos": [
    {{"titulo": "Titulo", "query": "SELECT col1, SUM(col2) as total FROM tabla GROUP BY col1 ORDER BY total DESC LIMIT 10", "tipo": "bar", "descripcion": "Que muestra"}},
    {{"titulo": "Titulo 2", "query": "SELECT col1, COUNT(*) as total FROM tabla GROUP BY col1", "tipo": "pie", "descripcion": "Que muestra"}}
  ]
}}

Reglas:
- Genera exactamente 4 KPIs y 4 gráficos
- Tipos disponibles: bar, line, pie, scatter
- Usa SOLO tablas y columnas del esquema
- Las queries deben ser SQL válido para SQLite
- Los iconos deben ser emojis relevantes

Esquema:
{schema_str}
"""
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    raw = respuesta.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

def crear_grafico(df, tipo, titulo):
    cols_num = df.select_dtypes(include='number').columns.tolist()
    cols_cat = df.select_dtypes(include='object').columns.tolist()

    if df.empty or len(df.columns) < 2:
        return None

    col_x = cols_cat[0] if cols_cat else df.columns[0]
    col_y = cols_num[0] if cols_num else df.columns[1]

    try:
        if tipo == "bar":
            fig = px.bar(
                df, x=col_x, y=col_y, title=titulo,
                color=col_x,
                color_discrete_sequence=SECUENCIA_COLORES,
                text=col_y
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(**LAYOUT_BASE)

        elif tipo == "line":
            fig = px.line(
                df, x=col_x, y=col_y, title=titulo,
                color_discrete_sequence=SECUENCIA_COLORES,
                markers=True
            )
            fig.update_traces(line=dict(width=3))
            fig.update_layout(**LAYOUT_BASE)

        elif tipo == "pie":
            fig = px.pie(
                df, names=col_x, values=col_y, title=titulo,
                color_discrete_sequence=SECUENCIA_COLORES,
                hole=0.4
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Valor: %{value:,}<br>Porcentaje: %{percent}"
            )
            fig.update_layout(**{k: v for k, v in LAYOUT_BASE.items() if k not in ['xaxis', 'yaxis']})

        elif tipo == "scatter":
            fig = px.scatter(
                df, x=col_x, y=col_y, title=titulo,
                color=col_x,
                color_discrete_sequence=SECUENCIA_COLORES,
                size=col_y if col_y in cols_num else None
            )
            fig.update_layout(**LAYOUT_BASE)

        else:
            fig = px.bar(df, x=col_x, y=col_y, title=titulo,
                        color_discrete_sequence=SECUENCIA_COLORES)
            fig.update_layout(**LAYOUT_BASE)

        return fig

    except Exception:
        return None

def calcular_kpis(df):
    kpis = []
    cols_numericas = df.select_dtypes(include='number').columns.tolist()
    kpis.append({"nombre": "Total filas", "valor": f"{len(df):,}", "icono": "📦", "descripcion": "Registros totales"})
    kpis.append({"nombre": "Total columnas", "valor": len(df.columns), "icono": "📋", "descripcion": "Variables disponibles"})
    for col in cols_numericas[:2]:
        kpis.append({"nombre": f"Total {col}", "valor": f"{df[col].sum():,.2f}", "icono": "💰", "descripcion": f"Suma de {col}"})
        kpis.append({"nombre": f"Media {col}", "valor": f"{df[col].mean():,.2f}", "icono": "📈", "descripcion": f"Promedio de {col}"})
    return kpis

def generar_grafico_personalizado(df, tipo, col_x, col_y, color, titulo):
    COLORES_SOLIDOS = {
        "Azul": "#4FC3F7", "Rojo": "#EF9A9A",
        "Verde": "#81C784", "Naranja": "#FFB74D",
        "Morado": "#CE93D8", "Gris": "#B0BEC5"
    }
    color_solido = COLORES_SOLIDOS.get(color, "#4FC3F7")

    try:
        if tipo == "Barras":
            fig = px.bar(df, x=col_x, y=col_y, title=titulo,
                        color=col_x, color_discrete_sequence=SECUENCIA_COLORES, text=col_y)
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        elif tipo == "Línea":
            fig = px.line(df, x=col_x, y=col_y, title=titulo,
                         color_discrete_sequence=[color_solido], markers=True)
            fig.update_traces(line=dict(width=3))
        elif tipo == "Pie":
            fig = px.pie(df, names=col_x, values=col_y, title=titulo,
                        color_discrete_sequence=SECUENCIA_COLORES, hole=0.4)
        elif tipo == "Scatter":
            fig = px.scatter(df, x=col_x, y=col_y, title=titulo,
                           color_discrete_sequence=[color_solido])
        elif tipo == "Área":
            fig = px.area(df, x=col_x, y=col_y, title=titulo,
                         color_discrete_sequence=[color_solido])
        else:
            fig = px.bar(df, x=col_x, y=col_y, title=titulo)

        fig.update_layout(**LAYOUT_BASE)
        return fig
    except Exception:
        return None

COLORES = {
    "Azul": "Blues", "Rojo": "Reds", "Verde": "Greens",
    "Naranja": "Oranges", "Morado": "Purples", "Gris": "Greys"
}