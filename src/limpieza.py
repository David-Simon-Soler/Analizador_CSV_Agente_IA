import pandas as pd

def limpiar_datos(columnas, filas):
    df = pd.DataFrame(filas, columns=columnas)
    
    reporte = []
    
    # 1. Duplicados
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        df = df.drop_duplicates()
        reporte.append(f"🗑️ Eliminados {duplicados} duplicados")
    
    # 2. Nulos
    nulos = df.isnull().sum()
    for col, cantidad in nulos.items():
        if cantidad > 0:
            if df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(0)
                reporte.append(f"🔢 Columna '{col}': {cantidad} nulos rellenados con 0")
            else:
                df[col] = df[col].fillna("desconocido")
                reporte.append(f"📝 Columna '{col}': {cantidad} nulos rellenados con 'desconocido'")
    
    # 3. Detectar columnas de fecha
    for col in df.columns:
        if any(palabra in col.lower() for palabra in ['date', 'timestamp', 'fecha']):
            try:
                df[col] = pd.to_datetime(df[col])
                reporte.append(f"📅 Columna '{col}' convertida a formato fecha")
            except:
                pass
    
    # 4. Detectar columnas numéricas como texto
    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_numeric(df[col])
                reporte.append(f"🔢 Columna '{col}' convertida a número")
            except:
                pass
    
    return df, reporte