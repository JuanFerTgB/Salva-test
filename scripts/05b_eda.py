import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_raw = pd.read_csv("data/raw/pacientes.csv")
df_clean = pd.read_csv("data/clean/pacientes_clean.csv")

# Resumen calidad

resumen_calidad = pd.DataFrame({
    "filas_totales": [len(df_raw), len(df_clean)],
    "ids_unicos": [df_raw["id_paciente"].nunique(), df_clean["id_paciente"].nunique()],
    "nulos_edad": [df_raw["edad_paciente"].isnull().sum(), df_clean["edad_paciente"].isnull().sum()],
    "nulos_sexo": [df_raw["sexo"].isnull().sum(), df_clean["sexo"].isnull().sum()],
    "nulos_peso": [df_raw["peso_kg"].isnull().sum(), df_clean["peso_kg"].isnull().sum()],
    "nulos_altura": [df_raw["altura_cm"].isnull().sum(), df_clean["altura_cm"].isnull().sum()],
    "edades_fuera_rango": [
        ((df_raw["edad_paciente"] < 0) | (df_raw["edad_paciente"] > 120)).sum(),
        ((df_clean["edad_paciente"] < 0) | (df_clean["edad_paciente"] > 120)).sum()
    ],
}, index=["Antes (raw)", "Después (clean)"])

print(resumen_calidad.T)
resumen_calidad.T.to_csv("reports/figures/resumen_calidad_antes_despues.csv")

df = pd.read_csv("data/clean/pacientes_clean.csv")
df["etiqueta_bin"] = (df["etiqueta"] == "Anormal").astype(int)

numericas = ["edad_paciente", "peso_kg", "altura_cm", "frecuencia_cardiaca_media_bpm", "etiqueta_bin"]

plt.figure(figsize=(6, 5))
sns.heatmap(df[numericas].corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Correlación de variables clínicas con la etiqueta (Anormal=1)")
plt.savefig("reports/figures/06b_correlacion_con_etiqueta.png", dpi=120, bbox_inches="tight")
plt.close()

# Estadísticas descriptivas agrupadas 
print(df.groupby("etiqueta")[["edad_paciente", "peso_kg", "altura_cm", "frecuencia_cardiaca_media_bpm"]].describe().T)

# Correlaciones explicitas

correlaciones = df[["edad_paciente", "peso_kg", "altura_cm", "frecuencia_cardiaca_media_bpm", "etiqueta_bin"]].corr()["etiqueta_bin"].sort_values(ascending=False)
print(correlaciones)

tabla_sexo = pd.crosstab(df["sexo"], df["etiqueta"], normalize="index") * 100
print(tabla_sexo.round(1))

df["grupo_edad"] = pd.cut(df["edad_paciente"], bins=[0, 40, 60, 80, 120], labels=["<40", "40-60", "60-80", "80+"])
tabla_edad = pd.crosstab(df["grupo_edad"], df["etiqueta"], normalize="index") * 100
print(tabla_edad.round(1))

plt.figure(figsize=(7, 5))
sns.scatterplot(data=df, x="edad_paciente", y="frecuencia_cardiaca_media_bpm", hue="etiqueta", alpha=0.6)
plt.title("Frecuencia cardíaca vs Edad, por etiqueta")
plt.savefig("reports/figures/08_fc_vs_edad_por_etiqueta.png", dpi=120, bbox_inches="tight")
plt.close()