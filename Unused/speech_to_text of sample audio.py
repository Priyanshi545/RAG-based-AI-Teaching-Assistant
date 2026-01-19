import whisper 
import json
model=whisper.load_model("large-v2")
result=model.transcribe(audio="audios/sample_audio.mp3",language="en",task="transcribe",word_timestamps=False)
chunks=[]
for segment in result["segments"]:
    chunks.append({"id":segment["id"],"start":segment["start"],"end":segment["end"],"text":segment["text"]})
print(chunks)
with open("output.json","w") as f:
    json.dump(chunks,f)
    

 