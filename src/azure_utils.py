import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO

load_dotenv()

def get_container_client(container_name="data-salvahealth"):
    """Conectar con contenedor de Azure Blob Storage."""
    conn_str = os.getenv("AZURE_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("No se encontró AZURE_CONNECTION_STRING. Revisar .env")
    blob_service = BlobServiceClient.from_connection_string(conn_str)
    return blob_service.get_container_client(container_name)


def leer_csv_desde_blob(container_client, blob_name):
    """Descarga un blob y lo carga como DataFrame de pandas."""
    blob_data = container_client.download_blob(blob_name).readall()
    return pd.read_csv(BytesIO(blob_data))


def listar_blobs(container_client, prefix=""):
    """Lista los nombres de blobs, opcionalmente filtrados por carpeta."""
    return [b.name for b in container_client.list_blobs(name_starts_with=prefix)]

