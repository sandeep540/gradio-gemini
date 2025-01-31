from google import genai
import os
import time
import gradio as gr

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "scs-d-aiml-data-explorer-dev")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
MODEL_ID = os.environ.get("MODEL_ID", "gemini-2.0-flash-exp") 

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# Create a chat
chat = client.chats.create(model=MODEL_ID)

# Transform Gradio history to Gemini format
def transform_history(history):
    new_history = []
    for chat in history:
        new_history.append({"parts": [{"text": chat[0]}], "role": "user"})
        new_history.append({"parts": [{"text": chat[1]}], "role": "model"})
    return new_history

def response(message, history):
    global chat
    # The history will be the same as in Gradio, the 'Undo' and 'Clear' buttons will work correctly.
    chat.history = transform_history(history)
    response = chat.send_message(message)
    response.resolve()

    # Each character of the answer is displayed
    for i in range(len(response.text)):
        time.sleep(0.05)
        yield response.text[: i+1]
        
gr.ChatInterface(response, title='Gemini Chat', textbox=gr.Textbox(placeholder="Question to Gemini")).launch(debug=True)
