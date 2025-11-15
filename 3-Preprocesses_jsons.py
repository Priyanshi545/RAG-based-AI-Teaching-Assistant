import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def create_embedding(text_list):
 r=requests.post("http://localhost:11434/api/embed", json={
    "model":"qllama/bge-small-en-v1.5",
    "input":text_list
 })

 embedding=r.json()["embeddings"]
 return embedding


jsons=os.listdir('jsons')
my_dict=[]
chunk_id=0

for json_file in jsons:
  
  with open(f"jsons/{json_file}") as f:
    content=json.load(f)
    print(f"Creating embedding for {json_file}")
    embeddings=create_embedding([c['text'] for c in content['chunks']])

  for i,chunk in enumerate(content["chunks"]):
    chunk['chunk_id']=chunk_id
    chunk['embedding']=embeddings[i]
    chunk_id+=1
    my_dict.append(chunk)

    


df =pd.DataFrame.from_records(my_dict) 
print(df)

# Save this dataframe
joblib.dump(df,'embeddings.joblib')


# print(np.vstack(df['embedding'].values))
# print(np.vstack(df["embedding"]).shape)

# print(my_dict)
# pd.DataFrame.from_records() is a Pandas constructor that creates a DataFrame from a list of records — where each record is typically a dictionary, tuple, or list representing a row.

# a=create_embedding("the cat sat on the mat")
# print(a[0:5])