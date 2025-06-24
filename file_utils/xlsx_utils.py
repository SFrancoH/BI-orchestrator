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

def xlsx2json(input_folder="data", output_folder="data"):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if file.lower().endswith(".xlsx"):
            path_xlsx = os.path.join(input_folder, file)
            try:
                sheets = pd.read_excel(path_xlsx, sheet_name=None)
                df = pd.concat(sheets.values(), ignore_index=True) if isinstance(sheets, dict) else sheets

                # Convertir fechas a texto ISO
                for col, dt in df.dtypes.items():
                    if pd.api.types.is_datetime64_any_dtype(dt):
                        df[col] = df[col].dt.strftime('%Y-%m-%d')

                # Renombrar columna si es "contact.xlsx"
                if file.lower() == "contact.xlsx":
                    if "Record ID" in df.columns:
                        df.rename(columns={"Record ID": "Contact id"}, inplace=True)

                json_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".json")
                df.to_json(json_path, orient="records", force_ascii=False, indent=4, date_format="iso")
                print(f"✅ '{file}' → '{os.path.basename(json_path)}'")
            except Exception as e:
                print(f"❌ Error en '{file}': {e}")