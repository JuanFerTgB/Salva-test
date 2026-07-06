import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from azure_utils import get_container_client, leer_csv_desde_blob, listar_blobs
import pandas as pd

container_client = get_container_client(container_name="data-salvahealth")

# 1. Cargar datos de pacientes
print("Cargando pacientes.csv...")
df_pacientes = leer_csv_desde_blob(container_client, "pacientes.csv")
print(f"Pacientes cargados: {df_pacientes.shape[0]} filas, {df_pacientes.shape[1]} columnas")
print(df_pacientes.head())

# 2. Cargar todas las señales ECG
print("\nCargando señales ECG (esto puede tardar un par de minutos)...")
signal_blobs = listar_blobs(container_client, prefix="signals/")
print(f"Archivos de señal encontrados: {len(signal_blobs)}")

signals = {}
for i, blob_name in enumerate(signal_blobs):
    df_signal = leer_csv_desde_blob(container_client, blob_name)
    patient_id = blob_name.split("/")[-1].replace(".csv", "")
    signals[patient_id] = df_signal
    if (i + 1) % 50 == 0:
        print(f"  {i + 1}/{len(signal_blobs)} señales cargadas...")

print(f"\n✅ Total de señales cargadas: {len(signals)}")