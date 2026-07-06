import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from azure_utils import get_container_client, leer_csv_desde_blob, listar_blobs
import pandas as pd

container_client = get_container_client(container_name="data-salvahealth")

df_pacientes = leer_csv_desde_blob(container_client, "pacientes.csv")
signal_blobs = listar_blobs(container_client, prefix="signals/")
ids_con_senal = set(b.split("/")[-1].replace(".csv", "") for b in signal_blobs)

print(f"Total filas en pacientes.csv: {len(df_pacientes)}")
print(f"Total ids únicos en pacientes.csv: {df_pacientes['id_paciente'].nunique()}")
print(f"Duplicados en id_paciente: {df_pacientes['id_paciente'].duplicated().sum()}")

ids_pacientes = set(df_pacientes['id_paciente'])
sin_senal = ids_pacientes - ids_con_senal
sin_paciente = ids_con_senal - ids_pacientes

# Ver el contenido real de los duplicados
duplicados = df_pacientes[df_pacientes['id_paciente'].duplicated(keep=False)]
duplicados_ordenados = duplicados.sort_values('id_paciente')
print(duplicados_ordenados)

print(f"\nPacientes sin señal ECG: {len(sin_senal)}")
print(list(sin_senal)[:10])

print(f"\nSeñales sin paciente correspondiente: {len(sin_paciente)}")
print(list(sin_paciente)[:10])

