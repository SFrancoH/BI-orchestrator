# file_utils/xlsx_utils.py
import os
import pandas as pd

def read_xlsx(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ No se encontró el archivo: {path}")

    df = pd.read_excel(path)  # lee la primera hoja por defecto
    print(f"✅ Leído '{path}': {df.shape[0]} filas y {df.shape[1]} columnas.")
    return df

def get_first_column_ids(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ No existe: {path}")
    df = pd.read_excel(path, header=0, dtype=str)
    first_col = df.iloc[:, 0].dropna().unique().tolist()
    print(f"✅ {len(first_col)} IDs extraídos de la primera columna.")
    return first_col

def save_xlsx_incremental(df, filename):
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", filename)

    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.drop_duplicates(subset=["date_start", "ad_id"], inplace=True)
    else:
        combined_df = df

    combined_df.to_excel(file_path, index=False)
    print(f"💾 Datos guardados/actualizados en: {file_path}")
