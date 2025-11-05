import os
import io
import json
import pandas as pd
import azure.functions as func
from azure.storage.blob import BlobServiceClient

DEFAULT_CONN = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/"
    "K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
    "TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
)

OUTPUT_PATH = os.environ.get("SIMULATED_NOSQL_PATH", "simulated_nosql/results.json")
CONTAINER_NAME = os.environ.get("DATASET_CONTAINER", "datasets")
BLOB_NAME = os.environ.get("DATASET_BLOB", "All_Diets.csv")


def _get_blob_bytes(container: str, blob: str, conn_str: str) -> bytes:
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_client = blob_service_client.get_container_client(container)
    blob_client = container_client.get_blob_client(blob)
    return blob_client.download_blob().readall()


def _process_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(
        columns={
            "Protein (g)": "Protein(g)",
            "Carbs (g)": "Carbs(g)",
            "Fat (g)": "Fat(g)",
        }
    )
    for c in ["Protein(g)", "Carbs(g)", "Fat(g)"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df.fillna(df.mean(numeric_only=True), inplace=True)
    avg_macros = (
        df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]]
        .mean()
        .reset_index()
        .sort_values("Diet_type")
    )
    return avg_macros


def main(inputBlob: func.InputStream):
    conn = os.environ.get("AZURE_STORAGE_CONNECTION_STRING", DEFAULT_CONN)

    try:
        raw = inputBlob.read()
        df = pd.read_csv(io.BytesIO(raw))
    except Exception:
        csv_bytes = _get_blob_bytes(CONTAINER_NAME, BLOB_NAME, conn)
        df = pd.read_csv(io.BytesIO(csv_bytes))

    avg_macros = _process_df(df)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(avg_macros.to_dict(orient="records"), f, indent=2)

    print(f"saved results to {OUTPUT_PATH}")
