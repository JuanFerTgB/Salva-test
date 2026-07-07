import pandas as pd
import numpy as np
import re ,os
import pickle

df = pd.read_csv("data/raw/pacientes.csv")

# Estandarizar fechas formato AÑO/MES/DIA
def parsear_fecha(f):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%B %d, %Y"):
        try:
            return pd.to_datetime(f, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["fecha_registro"] = df["fecha_registro"].apply(parsear_fecha)
print(f"Fechas no parseadas tras estandarizar: {df['fecha_registro'].isnull().sum()}")

# Marcar edades imposibles como NaN
df.loc[(df["edad_paciente"] < 0) | (df["edad_paciente"] > 120), "edad_paciente"] = np.nan

# COnservar la fila más completa por id_paciente 
df["completitud"] = df.notna().sum(axis=1)
df = df.sort_values(["id_paciente", "completitud", "fecha_registro"], ascending=[True, False, False])
df = df.drop_duplicates(subset="id_paciente", keep="first")
df = df.drop(columns="completitud")

print(f"Filas tras deduplicar: {len(df)}")  

# Imputar nulos restantes 
df["edad_paciente"] = df["edad_paciente"].fillna(df["edad_paciente"].median())
df["peso_kg"] = df["peso_kg"].fillna(df["peso_kg"].median())
df["altura_cm"] = df["altura_cm"].fillna(df["altura_cm"].median())
df["sexo"] = df["sexo"].fillna("Desconocido")

# Verificación final 
print("\nNulos restantes:")
print(df.isnull().sum())
print(f"\nFilas finales: {len(df)}")

# Guardar como dataset limpio 
df.to_csv("data/clean/pacientes_clean.csv", index=False)
print("\nGuardado en data/clean/pacientes_clean.csv")





