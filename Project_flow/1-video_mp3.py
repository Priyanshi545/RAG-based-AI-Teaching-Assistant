# The subprocess module in Python is like a bridge between your Python code and the command-line interface (CLI). It lets you run external programs or shell commands directly from your Python script.
# Why Use It?
# - Automates tasks that normally require manual command-line work
# - Integrates powerful tools (like ffmpeg, ImageMagick, or curl) into Python workflows
# - Makes your scripts more flexible and capable
#  What Does subprocess Do?
# - Launches external applications (like ffmpeg, git, or even system commands like ls, dir, etc.)
# - Captures output from those commands (if needed)
# - Handles errors and return codes
# - Allows interaction with the process (e.g., sending input or reading output)


# Th os module acts as a bridge between Python and the underlying operating system. It allows you to:
# - Navigate the file system
# - Manage files and directories
# - Access environment variables
# - Control processes and permissions
# This makes it essential for scripting, automation, and system-level programming.

# Commonly Used Functions 
# os.getcwd():- it give you the name of the current working directories 
#  os.listdir(path):- it give you the list of the all enteries in the directories by giving their path to it
#  os.mkdir(path):- it create a new directories(file,folder)
#  os.remove(path):- it is used to remove any directories
#  os.rename(src, dst):- used to rename any files or folder
#  os.path.exists(path):- it checks if the path of the following directories is exist or not
#  os.environ:- it access the environment variables
#  os.system(cmd):- executes a shell command 


# It will convert all the video file that is in mp4 to audio files that is in mp3
import os
import subprocess
file=os.listdir("Videos")
for file in file:
    # print(file)
    audio_number=file.split("_")[0]
    audio_name=file.split("_")[1][:-4]
    # print(audio_number,  audio_name)
    subprocess.run(["ffmpeg",  "-i", f"Videos/{file}", f"audios/{audio_number}_{audio_name}.mp3"])
    # subprocess.run["ffmpeg", "-i", f"audios/" -t 10 -c:a copy output.mp3]