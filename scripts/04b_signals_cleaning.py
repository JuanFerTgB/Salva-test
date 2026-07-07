import pickle
import pandas as pd
import numpy as np
import os

# Cargar señales crudas
with open("data/raw/signals.pkl", "rb") as f:
    signals = pickle.load(f)

print(f"Total de señales cargadas: {len(signals)}")

# Caso conocido (identificado mediante los detalles e los datos codigo 03): P0011 vs P00011 
# Se identificó que P00011 es un archivo duplicado de P0011 en el storage.
# Se verifica que sean idénticas antes de descartar una.
print("\n¿Existe P0011?", "P0011" in signals)
print("¿Existe P00011?", "P00011" in signals)

if "P0011" in signals and "P00011" in signals:
    sig_0011 = signals["P0011"]
    sig_00011 = signals["P00011"]
    print("Shape P0011:", sig_0011.shape)
    print("Shape P00011:", sig_00011.shape)
    print("¿Son idénticas?", sig_0011.equals(sig_00011))

    if sig_0011.equals(sig_00011):
        del signals["P00011"]
        print("P00011 descartada por ser duplicado exacto de P0011.")

print(f"Total de señales tras descartar duplicado: {len(signals)}")

# Diagnóstico de calidad sobre el resto de señales
reporte = []
for pid, sig in signals.items():
    reporte.append({
        "id_paciente": pid,
        "n_filas": len(sig),
        "nulos_ecg": sig["ecg_mV"].isnull().sum(),
        "nulos_tiempo": sig["t_seg"].isnull().sum(),
        "varianza_ecg": sig["ecg_mV"].var(),
        "min_ecg": sig["ecg_mV"].min(),
        "max_ecg": sig["ecg_mV"].max(),
        "duracion_seg": sig["t_seg"].max() - sig["t_seg"].min(),
    })

df_reporte = pd.DataFrame(reporte)

print("\nLongitudes distintas a 2500:")
print(df_reporte[df_reporte["n_filas"] != 2500])

print("\nSeñales con nulos:")
print(df_reporte[(df_reporte["nulos_ecg"] > 0) | (df_reporte["nulos_tiempo"] > 0)])

print("\nSeñales planas o casi planas (varianza sospechosamente baja):")
print(df_reporte[df_reporte["varianza_ecg"] < 0.0001])

print("\nSeñales con voltajes fuera de rango fisiológico (±5 mV):")
print(df_reporte[(df_reporte["min_ecg"] < -5) | (df_reporte["max_ecg"] > 5)])

print("\nResumen general:")
print(df_reporte[["n_filas", "varianza_ecg", "min_ecg", "max_ecg", "duracion_seg"]].describe())

# Guardar señales limpias
os.makedirs("data/clean", exist_ok=True)
with open("data/clean/signals_clean.pkl", "wb") as f:
    pickle.dump(signals, f)

print("\nSeñales limpias guardadas en data/clean/signals_clean.pkl")





