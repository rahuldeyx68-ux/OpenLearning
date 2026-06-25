import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)

HF_TOKEN = os.getenv('HF_TOKEN')
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DESMOS_API_KEY = os.getenv('DESMOS_API_KEY')

API_KEY = HF_TOKEN or NVIDIA_API_KEY or GEMINI_API_KEY
if not API_KEY:
    raise RuntimeError(f'Missing HF_TOKEN, NVIDIA_API_KEY, or GEMINI_API_KEY in environment. Tried loading {dotenv_path}')

if not DESMOS_API_KEY:
    raise RuntimeError(f'Missing DESMOS_API_KEY in environment. Tried loading {dotenv_path}')

use_huggingface = bool(HF_TOKEN)
base_url = 'https://router.huggingface.co/v1' if use_huggingface else 'https://integrate.api.nvidia.com/v1'
model = 'nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16:deepinfra' if use_huggingface else 'nvidia/nemotron-3-ultra-550b-a55b'

client = OpenAI(base_url=base_url, api_key=API_KEY)
app = Flask(__name__, template_folder='templates')

def serve_html_with_api_key(filename):
    """Serve HTML file with Desmos API key injected from environment."""
    filepath = os.path.join(ROOT_DIR, 'templates', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content.replace('DESMOS_API_KEY', DESMOS_API_KEY)

@app.route('/', methods=['GET'])
def index():
    return serve_html_with_api_key('index.htm')

@app.route('/graph', methods=['GET'])
def graph():
    return serve_html_with_api_key('graph.htm')

@app.route('/geometry', methods=['GET'])
def geometry():
    return serve_html_with_api_key('geometry.htm')

@app.route('/cal', methods=['GET'])
def cal():
    return serve_html_with_api_key('calculator.htm')

@app.route('/ai', methods=['GET'])
def ai_chat():
    filepath = os.path.join(ROOT_DIR, 'ai_chat.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'error': 'No message provided.'}), 400

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You are a math tutor. Answer only math questions and explanation requests about graphs, algebra, geometry, and calculus. '
                        'If the user asks for non-math topics, politely say you can only help with math.'
                    )
                },
                {'role': 'user', 'content': message}
            ],
            temperature=0.25,
            max_tokens=512,
            top_p=0.9,
            **({'extra_body': {'chat_template_kwargs': {'enable_thinking': True}, 'reasoning_budget': 1024}} if not use_huggingface else {}),
        )

        reply = ''
        if completion.choices:
            choice = completion.choices[0]
            message_obj = getattr(choice, 'message', None)
            if message_obj:
                reply = getattr(message_obj, 'content', None) or (message_obj.get('content') if hasattr(message_obj, 'get') else None) or ''
            if not reply:
                reply = getattr(choice, 'text', '') or ''

        return jsonify({'reply': reply.strip()})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
