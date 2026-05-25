import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv
import pandas as pd

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def ejecutar_query(query, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()
    conn.close()
    return columnas, filas

def generar_query(pregunta, schema_texto):
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": schema_texto},
            {"role": "user", "content": pregunta}
        ]
    )
    return respuesta.choices[0].message.content.strip()

def consultar(pregunta, schema_texto, db_path):
    MAX_INTENTOS = 3
    for intento in range(MAX_INTENTOS):
        try:
            query = generar_query(pregunta, schema_texto)
            columnas, filas = ejecutar_query(query, db_path)
            df = pd.DataFrame(filas, columns=columnas)
            return query, df
        except Exception as e:
            if intento + 1 == MAX_INTENTOS:
                raise Exception(f"No se pudo ejecutar tras {MAX_INTENTOS} intentos: {e}")