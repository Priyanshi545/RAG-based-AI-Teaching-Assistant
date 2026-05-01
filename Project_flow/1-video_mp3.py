import os
import subprocess
file=os.listdir("Videos")
for file in file:
    # print(file)
    audio_number=file.split("_")[0]
    audio_name=file.split("_")[1][:-4]
    # print(audio_number,  audio_name)
    subprocess.run(["ffmpeg",  "-i", f"Videos/{file}", f"audios/{audio_number}_{audio_name}.mp3"])