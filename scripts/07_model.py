import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("reports/figures", exist_ok=True)

# dataset final (limpio + features)

df = pd.read_csv("data/features/pacientes_con_features.csv")

# Codificar variables categóricas
df["sexo_cod"] = df["sexo"].map({"M": 0, "F": 1, "Desconocido": 2})
df["etiqueta_bin"] = (df["etiqueta"] == "Anormal").astype(int)

FEATURES = [
    "edad_paciente", "peso_kg", "altura_cm", "sexo_cod",
    "frecuencia_cardiaca_media_bpm",
    "amplitud_qrs", "rmssd", "n_latidos_detectados"
]
X = df[FEATURES]
y = df["etiqueta_bin"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Random Forest

modelo = RandomForestClassifier(
    n_estimators=200, max_depth=6, random_state=42, class_weight="balanced"
)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

print("="*60)
print("RESULTADOS — Random Forest (dataset limpio + features)")
print("="*60)
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision (Anormal): {precision_score(y_test, y_pred):.3f}")
print(f"Recall (Anormal):    {recall_score(y_test, y_pred):.3f}")
print(f"F1 (Anormal):        {f1_score(y_test, y_pred):.3f}")
print()
print(classification_report(y_test, y_pred, target_names=["Normal", "Anormal"]))

# CM

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Normal", "Anormal"], yticklabels=["Normal", "Anormal"])
plt.ylabel("Real")
plt.xlabel("Predicho")
plt.title("Matriz de confusión — Random Forest")
plt.savefig("reports/figures/12_matriz_confusion.png", dpi=120, bbox_inches="tight")
plt.close()

# Importancia de features

importancias = pd.Series(modelo.feature_importances_, index=FEATURES).sort_values(ascending=False)
print("\nImportancia de features:")
print(importancias)

plt.figure(figsize=(7, 5))
importancias.plot(kind="barh")
plt.gca().invert_yaxis()
plt.title("Importancia de features — Random Forest")
plt.xlabel("Importancia")
plt.tight_layout()
plt.savefig("reports/figures/13_importancia_features.png", dpi=120, bbox_inches="tight")
plt.close()

# dataset CRUDO (sin limpiar) vs LIMPIO+features

print("\n" + "="*60)
print("COMPARACIÓN: crudo (sin limpiar) vs limpio + features")
print("="*60)

df_raw = pd.read_csv("data/raw/pacientes.csv")
df_raw["sexo_cod"] = df_raw["sexo"].map({"M": 0, "F": 1})  # nulos quedan como NaN, a propósito
df_raw["etiqueta_bin"] = (df_raw["etiqueta"] == "Anormal").astype(int)

FEATURES_RAW = ["edad_paciente", "peso_kg", "altura_cm", "sexo_cod", "frecuencia_cardiaca_media_bpm"]
X_raw = df_raw[FEATURES_RAW]
y_raw = df_raw["etiqueta_bin"]

X_raw = X_raw.fillna(X_raw.median())

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_raw, y_raw, test_size=0.2, random_state=42, stratify=y_raw
)

modelo_raw = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42, class_weight="balanced")
modelo_raw.fit(X_train_r, y_train_r)
y_pred_r = modelo_raw.predict(X_test_r)

print(f"Accuracy (crudo, sin features de señal):  {accuracy_score(y_test_r, y_pred_r):.3f}")
print(f"F1 Anormal (crudo):                       {f1_score(y_test_r, y_pred_r):.3f}")
print(f"\nAccuracy (limpio + features):             {accuracy_score(y_test, y_pred):.3f}")
print(f"F1 Anormal (limpio + features):            {f1_score(y_test, y_pred):.3f}")

# Comparación contra  baseline ingenuo 

print("\n" + "="*60)
print("COMPARACIÓN FINAL")
print("="*60)
print("Baseline ingenuo (1 umbral en amplitud_qrs): accuracy = 0.876, F1 Anormal = 0.86")
print(f"Random Forest (crudo, sin señal):            accuracy = {accuracy_score(y_test_r, y_pred_r):.3f}, F1 Anormal = {f1_score(y_test_r, y_pred_r):.3f}")
print(f"Random Forest (limpio + features de señal):  accuracy = {accuracy_score(y_test, y_pred):.3f}, F1 Anormal = {f1_score(y_test, y_pred):.3f}")



#  5 casos Anormales que el modelo falló en detectar
errores = X_test.copy()
errores["real"] = y_test
errores["predicho"] = y_pred
falsos_negativos = errores[(errores["real"] == 1) & (errores["predicho"] == 0)]
print(falsos_negativos)