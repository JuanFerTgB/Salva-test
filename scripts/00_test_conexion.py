import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from azure_utils import get_container_client

container_client = get_container_client()

print("Conectando a Azure Blob Storage")
blobs = list(container_client.list_blobs())
print(f"Blobs encontrados: {len(blobs)}")
for b in blobs[:15]: #los 15 primeros 
    print(" -", b.name)