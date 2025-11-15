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
    
#  Whisper is an open source model that is developed by Open AI that is used for the automatic speech recognization.It do variouus tasks such as transcribe audio to text(mean convert the audio to text), translate speech(convert speech of one language into text to other),identify spoken language,detech voice activity(determine the speech is present in audio or not)
# if you are doing the translation then dont used turbo model

# JSON (JavaScript Object Notation) is a lightweight data format used for storing and exchanging structured information. It’s easy for humans to read and write, and easy for machines to parse and generate.
# - Text-based: It represents data as plain text.
# - Structured: Uses key-value pairs and arrays.
# - Language-independent: Though derived from JavaScript, it's supported by nearly every programming language.
 