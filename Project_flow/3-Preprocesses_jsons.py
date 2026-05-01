import requests
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import joblib

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
OLLAMA_URL = "http://localhost:11434/api"

def ollama_request(endpoint, payload):
    try:
        r = requests.post(f"{OLLAMA_URL}/{endpoint}", json=payload, timeout=15)
        r.raise_for_status()
        response = r.json()
        if not isinstance(response, dict):
            raise ValueError("Unexpected Ollama response format")
        return response
    except requests.exceptions.RequestException as exc:
        raise RuntimeError("Unable to reach Ollama. Make sure Ollama is running on localhost:11434.") from exc


def create_embedding(text_list):
    response = ollama_request("embed", {
        "model":"nomic-embed-text",
        "input":text_list
    })
    embeddings = response.get("embeddings")
    if embeddings is None:
        raise RuntimeError("Ollama did not return embeddings. Check the model and input.")
    return embeddings

json_dir = ROOT_DIR / 'jsons'
if not json_dir.exists():
    raise FileNotFoundError(f"Could not find json directory: {json_dir}")

jsons = os.listdir(json_dir)
my_dict=[]
chunk_id=0

for json_file in jsons:
  
  with open(json_dir / json_file) as f:
    content=json.load(f)
    print(f"Creating embedding for {json_file}")
    embeddings=create_embedding([c['text'] for c in content['chunks']])

  for i,chunk in enumerate(content["chunks"]):
    chunk['chunk_id']=chunk_id
    chunk['embedding']=embeddings[i]
    chunk_id+=1
    my_dict.append(chunk)

    


df =pd.DataFrame.from_records(my_dict)

embeddings_path = ROOT_DIR / 'embeddings.joblib'
joblib.dump(df, embeddings_path)
print(f"Saved embeddings to {embeddings_path}")

