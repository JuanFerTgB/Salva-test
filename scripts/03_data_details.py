import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from azure_utils import get_container_client, leer_csv_desde_blob, listar_blobs
import pandas as pd
import pickle
import json


# Leer desde Azure  
container_client = get_container_client(container_name="data-salvahealth")

df = leer_csv_desde_blob(container_client, "pacientes.csv")

signal_blobs = listar_blobs(container_client, prefix="signals/")
signals = {}
for blob_name in signal_blobs:
    patient_id = blob_name.split("/")[-1].replace(".csv", "")
    signals[patient_id] = leer_csv_desde_blob(container_client, blob_name)

# Guardar copia local por seguridad (no es practico en sets de datos muy grandes)
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/pacientes.csv", index=False)
with open("data/raw/signals.pkl", "wb") as f:
    pickle.dump(signals, f)

# Diagnóstico de calidad
reporte = {}

reporte["filas_totales"] = len(df)
reporte["ids_unicos"] = df["id_paciente"].nunique()
reporte["filas_duplicadas_por_id"] = df["id_paciente"].duplicated().sum()

nulos = df.isnull().sum()
reporte["columnas_con_nulos"] = nulos[nulos > 0].to_dict()

reporte["edades_invalidas"] = df[(df["edad_paciente"] < 0) | (df["edad_paciente"] > 110)][["id_paciente", "edad_paciente"]].to_dict("records")
reporte["peso_invalido"] = df[(df["peso_kg"] <= 0) | (df["peso_kg"] > 300)][["id_paciente", "peso_kg"]].to_dict("records")
reporte["altura_invalida"] = df[(df["altura_cm"] <= 0) | (df["altura_cm"] > 230)][["id_paciente", "altura_cm"]].to_dict("records")
reporte["fc_invalida"] = df[(df["frecuencia_cardiaca_media_bpm"] <= 0) | (df["frecuencia_cardiaca_media_bpm"] > 250)][["id_paciente", "frecuencia_cardiaca_media_bpm"]].to_dict("records")

fechas_parseadas = pd.to_datetime(df["fecha_registro"], errors="coerce")
reporte["fechas_con_formato_raro"] = df.loc[fechas_parseadas.isnull(), ["id_paciente", "fecha_registro"]].to_dict("records")

reporte["valores_unicos_etiqueta"] = df["etiqueta"].value_counts(dropna=False).to_dict()
reporte["valores_unicos_sexo"] = df["sexo"].value_counts(dropna=False).to_dict()
reporte["valores_unicos_derivacion"] = df["derivacion_ecg"].value_counts(dropna=False).to_dict()

ids_pacientes = set(df["id_paciente"])
ids_con_senal = set(signals.keys())
reporte["pacientes_sin_senal"] = list(ids_pacientes - ids_con_senal)
reporte["senales_sin_paciente"] = list(ids_con_senal - ids_pacientes)

print(pd.Series(reporte))


## Ver todo sin truncar +
#for k, v in reporte.items():
#    print(f"\n{'='*50}")
#   print(k)
#    print('='*50)
#    if isinstance(v, (list, dict)):
#        print(json.dumps(v, indent=2, ensure_ascii=False, default=str))
#    else:
#        print(v)