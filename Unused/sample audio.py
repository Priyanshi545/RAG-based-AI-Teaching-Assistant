import subprocess
import os
input_path=f"audios/{"01_Introduction.mp3"}"
output_path=f"audios/{"sample_audio.mp3"}"
subprocess.run([
        "ffmpeg",
        "-i", input_path,
        "-t", "10",
        "-c:a", "copy",
        output_path
    ])