import requests
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib 
import json

df=joblib.load('embeddings.joblib')

def create_embedding(text_list):
 r=requests.post("http://localhost:11434/api/embed", json={
    "model":"qllama/bge-small-en-v1.5",
    "input":text_list
 })

 embedding=r.json()["embeddings"]
 return embedding

def inference(prompt):
 r=requests.post("http://localhost:11434/api/generate", json={
    "model":"llama3.2:3b",
    'prompt':prompt,
    "stream":False
 })

 response=r.json()
 print(response)
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

result=inference(prompt)["response"]
print(result)
with open("response.txt","w")as f:
 f.write(result)


# for index,item in new_df.iterrows():
#  print(index,item['number'],item['title'],item['start'],item['end'],item['text'])