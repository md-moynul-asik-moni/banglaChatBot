import requests
import json
import gradio as gr



from deep_translator import GoogleTranslator









url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt):

    prompt = GoogleTranslator(source='auto', target='en').translate(prompt)

    conversation_history.append(prompt)

    full_prompt = "\n".join(conversation_history)

    data = {
        "model": "llama2",
        "stream": False,
        "prompt": full_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        #response_text = GoogleTranslator(source='auto', target='bn').translate(response_text)
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return GoogleTranslator(source='auto', target='bn').translate(actual_response)
    else:
        print("Error:", response.status_code, response.text)
        return None

iface = gr.Interface(
    fn=generate_response,
    
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text"
)

iface.launch(share=True)