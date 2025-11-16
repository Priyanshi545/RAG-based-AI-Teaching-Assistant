## This is the following steps that you should follow to use this RAG based AI Teaching Assistance in your own data.

# Step1= Collect your videos
Collect the videos of any course or any playlist as a datasets and then move all that videos in a video folder

# Step2= Convert to mp3
Convert all your videos that is in mp4 to mp3 by running video_mp3 

# Step 3= Convert mp3 to json
Convert all the mp3 files to json by running the mp3_jsons

# Step 4= Convert the json files to vectors
Use the file preprocesses_jsons to convert this jsons files to a dataframe with embedding and then save it as a joblil pickle

# Step 5= Generating the prompt and feeding to LLM'S
Read the joblib file and load it to the memory.Then create the relevant prompt according to the user query and then pass it to the LLM's for generate the response 