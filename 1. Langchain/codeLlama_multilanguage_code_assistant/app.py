import gradio as gr
import requests
import json

url = "http://localhost:11434/api/generate"

headers = {
    "content-type": "application/json"
}

history = []

def generate_response(prompt):
    history.append(prompt)

    final_prompt = "\n".join(prompt)

    data = {
        "model": "codeguru",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url=url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response = response.text
        data = json.loads(response)

        actual_response = data['response']

        return actual_response
    else:
        print("error:", response.text)

# frontend

interface = gr.Interface(
    fn=generate_response,
    inputs=gr.TextArea(lines=4, placeholder="enter your prompt"),
    outputs="text"
)

interface.launch()