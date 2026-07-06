# Prueba Técnica — Salva Health

Pipeline de datos clínicos (variables + ECG) para clasificación binaria Normal/Anormal.

## Estructura del proyecto

- `data/raw/` — dataset original (en crudo)
- `data/clean/` — dataset post-limpieza
- `data/features/` — dataset con features, listo para modelar
- `scripts/` — scripts numerados por etapa del pipeline
- `src/` — funciones reutilizables (conexión a Azure, etc.)

## Diccionario de variables (`pacientes.csv`)

| Columna | Descripción |
|---|---|
| `id_paciente` | Identificador del paciente. |
| `edad_paciente` | Edad en años. |
| `sexo` | `M` / `F`. |
| `peso_kg` | Peso en kilogramos. |
| `altura_cm` | Altura en centímetros. |
| `fecha_registro` | Fecha de captura del registro. **Atención:** el formato no es uniforme en todo el archivo. |
| `frecuencia_cardiaca_media_bpm` | Frecuencia cardíaca media estimada, en latidos por minuto. |
| `derivacion_ecg` | Derivación del ECG registrada (constante: `II`). |
| `frecuencia_muestreo_hz` | Frecuencia de muestreo de la señal en `senales/` (constante: `250`). |
| `etiqueta` | Variable objetivo binaria: `Normal` / `Anormal`. |

## Origen y licencia

Este dataset fue preparado específicamente para este proceso de selección.
Las variables clínicas y la estructura están inspiradas en el dataset público
**PTB-XL** (Wagner et al., 2020, *Scientific Data*, PhysioNet, licencia
CC-BY 4.0 — https://physionet.org/content/ptb-xl/), pero los valores
concretos de este paquete son generados y no corresponden a pacientes
reales. No necesitas (ni debes) buscar este dataset específico en fuentes
públicas — no existe publicado en ningún otro lugar.

## Cómo correrlo

1. Instalar dependencias: `pip install -r requirements.txt`
2. Crear un archivo `.env` con tu connection string de Azure remplazando "AZURE_CONNECTION_STRING" con su clave personal
3. Ejecutar los scripts en orden desde `scripts/`

