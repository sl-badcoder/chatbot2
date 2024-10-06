from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENAI_API_KEY = 'dein_openai_api_key'  # Setze hier deinen OpenAI API-Schlüssel ein.
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'  # Die URL für die Chat Completion API.

def get_openai_response(message):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',  # Das Modell, das du verwenden möchtest.
        'messages': [{'role': 'user', 'content': message}],
        'max_tokens': 150  # Anzahl der maximalen Token in der Antwort.
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/send_message', methods=['POST'])
def send_message():
    content = request.json
    message = content.get('message')

    if not message:
        return jsonify({'error': 'Message is required.'}), 400

    # Hole die Antwort von OpenAI
    response_message = get_openai_response(message)
    return jsonify({'response': response_message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Server läuft auf localhost:5000
