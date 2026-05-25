<div align="center">

# 📊 Analizador CSV & Agente IA
### Creador de Dashboards Dinámicos con Lenguaje Natural

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq_API-F54E27?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![LLaMA](https://img.shields.io/badge/LLaMA_3.3-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://ai.meta.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br>

> **Transforma tus archivos CSV en dashboards ejecutivos interactivos simplemente describiendo lo que quieres ver — sin escribir una sola línea de código.**

<br>

![Interfaz](https://github.com/David-Simon-Soler/Analizador_CSV_Agente_IA/blob/main/Analizador_ai_csv.png)
![Uso Agente](https://github.com/David-Simon-Soler/Analizador_CSV_Agente_IA/blob/main/ejemplo_uso_agente_IA.png)
![Uso dashboard](https://github.com/David-Simon-Soler/Analizador_CSV_Agente_IA/blob/main/ejemplo_dashboard_agente_IA.png)
</div>

---

## 🚀 ¿Qué hace esta herramienta?

Este proyecto elimina la brecha entre los **datos en bruto** y las **decisiones de negocio**. Carga uno o varios archivos CSV, escribe tu pregunta en español, y el agente IA genera automáticamente visualizaciones interactivas con los resultados.

**Sin SQL. Sin código. Sin fricción.**

El sistema infiere relaciones entre tablas, ejecuta JOINs complejos en memoria y renderiza dashboards listos para presentar a dirección, todo en menos de un segundo.

---

## ✨ Características Principales

| Característica | Descripción |
|---|---|
| 🧠 **Agente IA con LLaMA 3.3** | Comprende consultas en lenguaje natural en español e infiere automáticamente las relaciones entre tablas |
| 🔗 **Análisis Multitabla** | Detecta claves foráneas y ejecuta JOINs automáticos entre múltiples CSVs simultáneamente |
| ⚡ **Baja Latencia** | Tiempos de respuesta inferiores a 1 segundo gracias a la infraestructura de Groq API |
| 📊 **Visualizaciones Interactivas** | Gráficos vectoriales con Plotly Express: hover, zoom, filtros y exportación incluidos |
| 🛡️ **Sin Riesgo de Inyección** | Arquitectura que elimina por diseño la ejecución de código malicioso en las consultas |
| 🗂️ **Dashboard Ejecutivo** | Panel consolidado donde se acumulan todos los análisis de la sesión en un único lienzo |
| 🔄 **Estado Persistente** | Gestión de sesión con `st.session_state` que mantiene los datos cargados entre interacciones |

---

## 🏗️ Arquitectura del Sistema

El sistema sigue un flujo lineal reactivo controlado en memoria, estructurado en cinco capas desacopladas:

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFAZ DE USUARIO                       │
│                   (Streamlit Frontend)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │  Archivos CSV + Pregunta en español
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           CAPA 1: INGESTA Y PERSISTENCIA DE ESTADO          │
│         Carga de archivos · st.session_state · Tipado       │
└───────────────────────┬─────────────────────────────────────┘
                        │  Metadatos: columnas, tipos, previews
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         CAPA 2: MOTOR DE MAPEO E INFERENCIA SEMÁNTICA       │
│       Extracción de esquemas · Detección de relaciones      │
└───────────────────────┬─────────────────────────────────────┘
                        │  Esquema estructurado + petición
                        ▼
┌─────────────────────────────────────────────────────────────┐
│      CAPA 3: COMPILADOR DE CONSULTAS DINÁMICAS (LLM)        │
│      LLaMA 3.3 via Groq · Inferencia FK · Plan Pandas       │
└───────────────────────┬─────────────────────────────────────┘
                        │  Código de transformación generado
                        ▼
┌─────────────────────────────────────────────────────────────┐
│          CAPA 4: PIPELINE DE PROCESAMIENTO EN CALIENTE      │
│     Pandas Engine · Normalización nulos · JOINs · Stats     │
└───────────────────────┬─────────────────────────────────────┘
                        │  DataFrame limpio y procesado
                        ▼
┌─────────────────────────────────────────────────────────────┐
│            CAPA 5: RENDERIZADO Y VISUALIZACIÓN              │
│        Plotly Express · Gráficos interactivos · Dashboard   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Rol |
|---|---|---|
| **Ecosistema Core** | Python 3.10+ | Orquestación del pipeline lógico y tipado estricto |
| **Orquestador IA** | Groq API + LLaMA 3.3 | Inferencia semántica y generación del plan de ejecución |
| **Manipulación OLAP** | Pandas | Limpieza de nulos, transformaciones temporales y JOINs indexados |
| **Lienzo Gráfico** | Plotly Express | Gráficos vectoriales interactivos con soporte nativo Hover |
| **Frontend Reactivo** | Streamlit | Interfaz de componentes con renderizado dinámico de datos |
| **Gestión de Entorno** | python-dotenv | Carga segura de variables de entorno y credenciales |

---

## 📋 Requisitos Previos

- Python **3.10 o superior**
- Una **API Key de Groq** (gratuita en [console.groq.com](https://console.groq.com))
- Git

---

## ⚙️ Instalación y Configuración Local

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/David-Simon-Soler/Analizador_CSV_Agente_IA.git
cd Analizador_CSV_Agente_IA
```

### Paso 2 — Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3 — Configurar credenciales

Crea un archivo `.env` en la raíz del proyecto (está protegido por `.gitignore` — **nunca se subirá a Git**):

```bash
# .env
GROQ_API_KEY=tu_clave_privada_groq_aqui
```

> 💡 Obtén tu API Key gratuita en [console.groq.com](https://console.groq.com). El tier gratuito es más que suficiente para uso personal.

### Paso 4 — Lanzar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## 🎯 Cómo Usar la Aplicación

1. **Carga tus archivos CSV** desde el panel lateral — puedes cargar múltiples archivos a la vez.
2. **El sistema analiza** automáticamente las columnas, tipos de datos y posibles relaciones entre tablas.
3. **Escribe tu pregunta en español** en el cuadro de chat. Por ejemplo:
   - *"¿Cuál es el promedio de ventas por categoría de producto?"*
   - *"Muéstrame los 10 clientes con mayor gasto total"*
   - *"¿Qué región tiene más pedidos en los últimos 3 meses?"*
4. **El Agente IA** procesa la consulta, ejecuta los JOINs necesarios y genera la visualización.
5. **Añade los gráficos al Dashboard Ejecutivo** para consolidar todos tus análisis en un solo panel.

---

## 📈 Caso de Estudio: Olist E-commerce Brazil

Para validar el sistema en condiciones reales de volumen empresarial, se cargaron simultáneamente tres datasets relacionales del ecosistema **Olist E-commerce Brazil**:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_customers_dataset.csv`

**Consulta introducida:**
> *"¿Cuál es el precio medio de los productos por categoría y qué estado compra más cada categoría?"*

**El agente ejecutó automáticamente un cuádruple INNER JOIN sobre más de 98.000 registros en segundos**, sin que el usuario escribiera código:

<div align="center">

| Métrica | Resultado |
|---|---|
| 📦 Registros procesados en caliente | **98.666 artículos** |
| 💰 Volumen total de facturación | **13.591.644,17 R$** |
| 🎯 Ticket medio por artículo | **137,75 R$** |
| ⚠️ Outlier máximo detectado | **6.735,00 R$** |

</div>

**Insight generado:** São Paulo (SP) y Río de Janeiro (RJ) concentran la mayor absorción de inventario premium. Este análisis, que normalmente requeriría scripts SQL complejos o pipelines ETL, estuvo disponible para toma de decisiones en **menos de 2 minutos**.

---

## 📁 Estructura del Proyecto

```
Analizador_CSV_Agente_IA/
│
├── app.py                  # Punto de entrada principal — aplicación Streamlit
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (NO incluido en Git)
├── .gitignore              # Protección de credenciales y archivos temporales
├── README.md               # Esta documentación
│
└── assets/                 # Recursos estáticos (imágenes, demos, etc.)
```

---

## 🔒 Seguridad y Privacidad

- Las credenciales de API **nunca se incluyen en el repositorio** gracias al archivo `.gitignore`.
- Todos los datos se procesan **exclusivamente en memoria local** — ningún dato de usuario sale de tu máquina.
- El agente IA opera sobre un esquema estructurado, lo que **elimina el riesgo de inyección de código** malicioso.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras un bug, tienes una idea de mejora o quieres añadir soporte para nuevos tipos de visualización:

1. Haz un **fork** del repositorio
2. Crea una rama: `git checkout -b feature/mi-mejora`
3. Haz commit de tus cambios: `git commit -m 'Add: descripción de la mejora'`
4. Haz push a la rama: `git push origin feature/mi-mejora`
5. Abre un **Pull Request**

---

## 👤 Autor

**David José Simón Soler**
*Data Analyst Junior*

[![Email](https://img.shields.io/badge/Email-davidsimonsoler2002%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:davidsimonsoler2002@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-David_Simón_Soler-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/david-josé-simón-soler-49992817b)
[![GitHub](https://img.shields.io/badge/GitHub-David--Simon--Soler-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/David-Simon-Soler)

<br>

*Si este proyecto te ha resultado útil, considera darle una ⭐ en GitHub.*

</div>
