from flask import Flask, request, render_template_string
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import joblib

app = Flask(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
EMBEDDINGS_FILE = SCRIPT_DIR.parent / 'embeddings.joblib'

try:
    df = joblib.load(EMBEDDINGS_FILE)
except FileNotFoundError:
    df = None
    app.logger.error(f"Could not find embeddings file: {EMBEDDINGS_FILE}")
except Exception as exc:
    df = None
    app.logger.error(f"Failed to load embeddings file: {exc}")

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
        app.logger.error(f"Ollama request failed: {exc}")
        raise RuntimeError("Unable to reach Ollama. Make sure Ollama is running on localhost:11434 and the required models are installed.")
    except ValueError as exc:
        app.logger.error(f"Ollama response parsing failed: {exc}")
        raise RuntimeError("Received an unexpected response from Ollama.")

def create_embedding(text_list):
    response = ollama_request("embed", {
        "model": "nomic-embed-text",
        "input": text_list
    }, timeout=60)
    embeddings = response.get("embeddings")
    if embeddings is None:
        raise RuntimeError("Ollama did not return embeddings. Check the model and server status.")
    return embeddings

def generate_response(prompt):
    response = ollama_request("generate", {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }, timeout=120)
    generated = response.get('response') or response.get('text')
    if not generated:
        raise RuntimeError("Ollama did not return a generated response. Check the model output format.")
    return generated

@app.route('/', methods=['GET', 'POST'])
def index():
    if df is None:
        return render_template_string(HTML_TEMPLATE, response="Embeddings are not loaded. Make sure 'embeddings.joblib' exists in the project root.")

    if request.method == 'POST':
        incoming_query = request.form['query']
        if not incoming_query.strip():
            return render_template_string(HTML_TEMPLATE, response="Please enter a valid question.")

        try:
            question_embedding = create_embedding([incoming_query])[0]
            similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
            top_result = 10
            max_idx = similarities.argsort()[::-1][:top_result]
            new_df = df.loc[max_idx]

            prompt = f'''I am teaching some concepts of python in this course. Here are the video subtitle chunks that contain the video number, title of the video, starting of the video in seconds, ending of the video in seconds and the text at that time.

{new_df[["title", "number", "text"]].to_json(orient="records")}

..................................................
"{incoming_query}"

The user asked this question related to the video chunks. Guide him by giving the correct answer of their question by telling him where the content is taught in the video and at which timestamp in a human way (don't use the above format it is just for you). Give the starting timestamp and the ending timestamp so that the user can easily go to that video. If the user asked any unrelated question than tell him that you can only give the answer related to this course and ask those questions that are related to the course.
'''

            response = generate_response(prompt)
        except RuntimeError as exc:
            response = str(exc)
        except Exception as exc:
            response = f"An unexpected error occurred: {exc}"

        return render_template_string(HTML_TEMPLATE, response=response)

    return render_template_string(HTML_TEMPLATE, response="")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG AI Teaching Assistance</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        form { margin-bottom: 20px; }
        input[type="text"] { width: 100%; padding: 10px; }
        button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .response { margin-top: 20px; padding: 10px; border: 1px solid #ddd; background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>RAG AI Teaching Assistance</h1>
    <p>Ask a question related to Python concepts taught in the videos.</p>
    <form method="post">
        <input type="text" name="query" placeholder="Enter your question here..." required>
        <button type="submit">Ask</button>
    </form>
    {% if response %}
    <div class="response">
        <h2>Response:</h2>
        <p>{{ response }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)