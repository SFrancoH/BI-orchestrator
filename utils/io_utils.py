import zipfile
import os
import shutil
import glob

def unzip_file(zip_path, extract_to="data"):
    """
    Extrae todos los archivos del ZIP en 'extract_to'.
    Retorna una lista con los paths de los archivos extraídos.
    """
    extracted_paths = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)
        extracted_paths = [os.path.join(extract_to, name) for name in z.namelist()]
    print(f"✅ Archivos extraídos: {extracted_paths}")
    return extracted_paths

def delete_zip_files(folder="data"):
    """
    Elimina todos los archivos con extensión .zip dentro de la carpeta 'data'.
    """
    if not os.path.isdir(folder):
        print(f"⚠️ La carpeta '{folder}' no existe.")
        return

    removed = 0
    for filename in os.listdir(folder):
        if filename.lower().endswith(".zip"):
            path = os.path.join(folder, filename)
            try:
                os.remove(path)
                print(f"🗑️ Eliminado: {path}")
                removed += 1
            except Exception as e:
                print(f"❌ No se pudo eliminar {path}: {e}")

    if removed == 0:
        print("📦 No se encontraron archivos .zip para eliminar.")
    else:
        print(f"✅ Se eliminaron {removed} archivos .zip.")

def rename_xlsx(old_path, new_name):
    """
    Renombra un archivo .xlsx manteniéndolo en su misma carpeta.

    Params:
    - old_path (str): ruta original del archivo, e.g. "data/deals_123.xlsx"
    - new_name (str): nuevo nombre del archivo, e.g. "deals_final.xlsx"

    Retorna:
    - new_path: ruta completa al archivo renombrado
    """
    if not os.path.isfile(old_path):
        raise FileNotFoundError(f"❌ No existe: {old_path}")

    folder = os.path.dirname(old_path)
    new_path = os.path.join(folder, new_name)

    os.rename(old_path, new_path)
    print(f"✅ Archivo renombrado: '{old_path}' → '{new_path}'")
    return new_path

def delete_all_xlsx(folder="data"):
    """
    Elimina todos los archivos .xlsx dentro de 'folder' y sus subdirectorios.
    """
    # Busca de forma recursiva los archivos .xlsx
    pattern = os.path.join(folder, '**', '*.xlsx')
    for file_path in glob.iglob(pattern, recursive=True):
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Eliminado: {file_path}")
            except Exception as e:
                print(f"❌ Error al eliminar {file_path}: {e}")
    print("✅ Proceso completado: todos los .xlsx han sido eliminados.")

def clean_data_folder(folder="data"):
    """
    Elimina todos los archivos y carpetas en 'folder',
    EXCEPTO los archivos con extensión .xlsx.
    """
    if not os.path.isdir(folder):
        print(f"⚠️ La carpeta '{folder}' no existe.")
        return

    for entry in os.listdir(folder):
        full_path = os.path.join(folder, entry)

        # Si es archivo y no termina en .xlsx → eliminarlo
        if os.path.isfile(full_path):
            if not entry.lower().endswith(".xlsx"):
                try:
                    os.remove(full_path)
                    print(f"🗑️ Archivo eliminado: {entry}")
                except Exception as e:
                    print(f"❌ No se pudo eliminar {entry}: {e}")

        # Si es carpeta → eliminarla completamente
        elif os.path.isdir(full_path):
            try:
                shutil.rmtree(full_path)
                print(f"📦 Carpeta eliminada: {entry}/")
            except Exception as e:
                print(f"❌ No se pudo eliminar carpeta {entry}/: {e}")
                
    print("✅ Limpieza completada: solo quedan archivos .xlsx (si había).")