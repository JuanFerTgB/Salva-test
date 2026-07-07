import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import find_peaks
import pickle
import os

# Cargar datos limpios
df_pacientes = pd.read_csv("data/clean/pacientes_clean.csv")
with open("data/clean/signals_clean.pkl", "rb") as f:
    signals = pickle.load(f)

# calcular features desde la señal ECG (signals)
def calcular_features_ecg(sig, altura_minima=0.5, distancia_min=50):
    picos, _ = find_peaks(sig["ecg_mV"], height=altura_minima, distance=distancia_min)
    tiempos_picos = sig["t_seg"].iloc[picos].values

    if len(tiempos_picos) >= 2:
        rr = np.diff(tiempos_picos)
        sdnn = rr.std()
        rmssd = np.sqrt(np.mean(np.diff(rr) ** 2)) if len(rr) >= 2 else np.nan
    else:
        sdnn, rmssd = np.nan, np.nan

    amplitud_qrs = sig["ecg_mV"].max() - sig["ecg_mV"].min()

    return {
        "n_latidos_detectados": len(picos),
        "sdnn": sdnn,
        "rmssd": rmssd,
        "amplitud_qrs": amplitud_qrs,
    }

resultados = []
for pid, sig in signals.items():
    feats = calcular_features_ecg(sig)
    feats["id_paciente"] = pid
    resultados.append(feats)

df_features = pd.DataFrame(resultados)

#  Merge con dataset de pacientes 
df = df_pacientes.merge(df_features, on="id_paciente", how="left")
df["etiqueta_bin"] = (df["etiqueta"] == "Anormal").astype(int)

#  Correlación con la etiqueta 
columnas_interes = [
    "edad_paciente", "frecuencia_cardiaca_media_bpm",
    "sdnn", "rmssd", "amplitud_qrs", "n_latidos_detectados",
    "etiqueta_bin"
]
correlaciones = df[columnas_interes].corr()["etiqueta_bin"].sort_values(ascending=False)
print("Correlación de cada variable con la etiqueta:\n")
print(correlaciones)

# Guardar dataset final con features 
os.makedirs("data/features", exist_ok=True)
df.to_csv("data/features/pacientes_con_features.csv", index=False)
print("\n✅ Dataset con features guardado en data/features/pacientes_con_features.csv")

# Grafica
os.makedirs("reports/figures", exist_ok=True)
sns.set_style("whitegrid")

features_a_graficar = ["amplitud_qrs", "sdnn", "rmssd", "frecuencia_cardiaca_media_bpm"]

fig, axes = plt.subplots(2, 2, figsize=(11, 8))
for ax, col in zip(axes.flatten(), features_a_graficar):
    sns.boxplot(data=df, x="etiqueta", y=col, ax=ax)
    ax.set_title(f"{col} por etiqueta")

plt.tight_layout()
plt.savefig("reports/figures/09_features_por_etiqueta.png", dpi=120, bbox_inches="tight")
plt.close()

# Bonus: los dos features más fuertes juntos en un scatter
plt.figure(figsize=(7, 5))
sns.scatterplot(data=df, x="amplitud_qrs", y="sdnn", hue="etiqueta", alpha=0.7)
plt.title("Amplitud QRS vs SDNN, por etiqueta")
plt.savefig("reports/figures/10_amplitud_vs_sdnn.png", dpi=120, bbox_inches="tight")
plt.close()

print("Gráficas guardadas en reports/figures/")




