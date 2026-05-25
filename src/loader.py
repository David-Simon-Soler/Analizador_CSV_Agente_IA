import pandas as pd
import sqlite3
import os
import tempfile

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')

def cargar_csvs(archivos_subidos):
    """
    Recibe una lista de archivos subidos desde Streamlit,
    los carga como DataFrames y los guarda en SQLite.
    Devuelve el esquema detectado automáticamente.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    esquema = {}
    
    for archivo in archivos_subidos:
        nombre_tabla = os.path.splitext(archivo.name)[0].lower().replace(" ", "_")
        
        df = pd.read_csv(archivo)
        
        # Limpiar nombres de columnas
        df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
        
        # Guardar en SQLite
        df.to_sql(nombre_tabla, conn, if_exists="replace", index=False)
        
        # Guardar esquema
        esquema[nombre_tabla] = {
            "columnas": list(df.columns),
            "tipos": df.dtypes.astype(str).to_dict(),
            "filas": len(df),
            "muestra": df.head(3).to_dict(orient="records")
        }
        
        print(f"✓ Tabla '{nombre_tabla}' cargada con {len(df)} filas y {len(df.columns)} columnas")
    
    conn.close()
    return esquema, DB_PATH

def generar_schema_texto(esquema):
    """
    Convierte el esquema detectado en texto para pasárselo al LLM.
    """
    texto = "Tienes acceso a una base de datos SQLite con las siguientes tablas:\n\n"
    
    for tabla, info in esquema.items():
        texto += f"- {tabla}: {', '.join(info['columnas'])}\n"
    
    texto += "\nGenera SOLO la query SQL, sin explicaciones, sin markdown, sin comillas al inicio o al final."
    
    return texto