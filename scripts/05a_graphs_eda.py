import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("reports/figures", exist_ok=True)

df = pd.read_csv("data/clean/pacientes_clean.csv")

sns.set_style("whitegrid")

# Visualizació variables clinicas

# Distribución de la etiqueta (Normal vs Anormal) 
plt.figure(figsize=(5, 4))
sns.countplot(data=df, x="etiqueta", palette=["#4C72B0", "#DD8452"])
plt.title("Distribución de etiqueta: Normal vs Anormal")
plt.savefig("reports/figures/01_distribucion_etiqueta.png", dpi=120, bbox_inches="tight")
plt.close()

# Edad
plt.figure(figsize=(6, 4))
sns.histplot(data=df, x="edad_paciente", bins=20, kde=True)
plt.title("Distribución de edad")
plt.savefig("reports/figures/02_distribucion_edad.png", dpi=120, bbox_inches="tight")
plt.close()

# Edad vs (normal/anormal)
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x="etiqueta", y="edad_paciente")
plt.title("Edad según etiqueta")
plt.savefig("reports/figures/03_edad_por_etiqueta.png", dpi=120, bbox_inches="tight")
plt.close()

# Sexo
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="sexo", hue="etiqueta")
plt.title("Sexo vs etiqueta")
plt.savefig("reports/figures/04_sexo_por_etiqueta.png", dpi=120, bbox_inches="tight")
plt.close()

# Frecuencia cardíaca por etiqueta 
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x="etiqueta", y="frecuencia_cardiaca_media_bpm")
plt.title("Frecuencia cardíaca media según etiqueta")
plt.savefig("reports/figures/05_fc_por_etiqueta.png", dpi=120, bbox_inches="tight")
plt.close()

# Matriz de correlación 
plt.figure(figsize=(6, 5))
numericas = df[["edad_paciente", "peso_kg", "altura_cm", "frecuencia_cardiaca_media_bpm"]]
sns.heatmap(numericas.corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Correlación entre variables numéricas")
plt.savefig("reports/figures/06_correlacion.png", dpi=120, bbox_inches="tight")
plt.close()

print("Gráficas de variables clínicas guardadas en reports/figures/")



# señales ECG Normal vs Anormal
import pickle
with open("data/clean/signals_clean.pkl", "rb") as f:
    signals = pickle.load(f)

ejemplo_normal = df[df["etiqueta"] == "Normal"]["id_paciente"].iloc[0]
ejemplo_anormal = df[df["etiqueta"] == "Anormal"]["id_paciente"].iloc[0]

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
axes[0].plot(signals[ejemplo_normal]["t_seg"], signals[ejemplo_normal]["ecg_mV"], color="#4C72B0")
axes[0].set_title(f"ECG Normal — Paciente {ejemplo_normal}")
axes[0].set_ylabel("mV")

axes[1].plot(signals[ejemplo_anormal]["t_seg"], signals[ejemplo_anormal]["ecg_mV"], color="#DD8452")
axes[1].set_title(f"ECG Anormal — Paciente {ejemplo_anormal}")
axes[1].set_ylabel("mV")
axes[1].set_xlabel("Tiempo (s)")

plt.tight_layout()
plt.savefig("reports/figures/07_ejemplo_ecg_normal_vs_anormal.png", dpi=120, bbox_inches="tight")
plt.close()

print("Ejemplo de señales ECG guardado en reports/figures/")