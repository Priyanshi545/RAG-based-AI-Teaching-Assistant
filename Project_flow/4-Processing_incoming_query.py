import requests
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import joblib 

SCRIPT_DIR = Path(__file__).resolve().parent
EMBEDDINGS_FILE = SCRIPT_DIR.parent / 'embeddings.joblib'

try:
    df = joblib.load(EMBEDDINGS_FILE)
except FileNotFoundError:
    print(f"Error: Could not find embeddings file at {EMBEDDINGS_FILE}")
    sys.exit(1)
except Exception as exc:
    print(f"Failed to load embeddings: {exc}")
    sys.exit(1)

OLLAMA_URL = "http://localhost:11434/api"

def ollama_request(endpoint, payload, timeout=120):
    try:
        r = requests.post(f"{OLLAMA_URL}/{endpoint}", json=payload, timeout=timeout)
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
    }, timeout=60)
    embeddings = response.get("embeddings")
    if embeddings is None:
        raise RuntimeError("Ollama did not return embeddings.")
    return embeddings


def inference(prompt):
    response = ollama_request("generate", {
        "model":"llama2",
        'prompt':prompt,
        "stream":False
    }, timeout=120)
    return response
 
incoming_query=input("Ask your question:")
question_embedding=create_embedding([incoming_query])[0]
# print(question_embedding)

similarities=cosine_similarity(np.vstack(df['embedding']),[question_embedding]).flatten()
# print(similarities)
top_reult=10
max_idx=similarities.argsort()[::-1][0:top_reult]
# print(max_idx)

new_df=df.loc[max_idx]
# print(new_df[['title','number','text',"id"]])

prompt=f''' I am teaching some concepts of python in this course.  Here are the video subtitle chunks that contain the video number,title of the video,starting of the video in the seconds,ending of the video in seconds and the text and the text at that time.

{new_df[["title","number","text"]].to_json(orient="records")}  # it will give you the list of dictionary

..................................................
"{incoming_query}"

The user asked this question related to the video chunks.Guide him by giving the correct answer of their question by telling him where the content is taught in the video and at which timestamp in a human way (dont used the above format it is just for you)  give the starting timestamp and the ending timestamp so that the user can easily go to that video. If the user asked any unrelated question than tell him that you can only give the answer related to this course and asked those question that is related to the course. 
'''

with open("prompt.txt","w")as f:
 f.write(prompt)

try:
    result_data = inference(prompt)
    result = result_data.get("response") or result_data.get("text") or str(result_data)
except Exception as exc:
    print(f"Error generating response: {exc}")
    result = "Failed to generate response"

print(result)
with open("response.txt","w")as f:
 f.write(result)



