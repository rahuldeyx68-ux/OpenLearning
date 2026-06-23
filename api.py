import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)
API_KEY = os.getenv('NVIDIA_API_KEY') or os.getenv('OPENAI_API_KEY')
DESMOS_API_KEY = os.getenv('DESMOS_API_KEY')

if not API_KEY:
    raise RuntimeError(f'Missing NVIDIA_API_KEY or OPENAI_API_KEY in environment. Tried loading {dotenv_path}')

if not DESMOS_API_KEY:
    raise RuntimeError(f'Missing DESMOS_API_KEY in environment. Tried loading {dotenv_path}')

client = OpenAI(
    base_url='https://integrate.api.nvidia.com/v1',
    api_key=API_KEY,
)

app = Flask(__name__, static_folder=None)

def serve_html_with_api_key(filename):
    """Serve HTML file with Desmos API key injected from environment"""
    filepath = os.path.join(ROOT_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    # Replace placeholder with actual API key
    html_content = html_content.replace('DESMOS_API_KEY', DESMOS_API_KEY)
    return html_content

@app.route('/', methods=['GET'])
def index():
    return serve_html_with_api_key('graph.htm')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'error': 'No message provided.'}), 400

    try:
        completion = client.chat.completions.create(
            model='nvidia/nemotron-3-ultra-550b-a55b',
            messages=[{'role': 'user', 'content': message}],
            temperature=1,
            top_p=0.95,
            max_tokens=1024,
            extra_body={
                'chat_template_kwargs': {'enable_thinking': True},
                'reasoning_budget': 1024,
            },
        )

        reply = ''
        if completion.choices:
            choice = completion.choices[0]
            reply = ''
            message_obj = getattr(choice, 'message', None)
            if message_obj:
                reply = getattr(message_obj, 'content', None) or (message_obj.get('content') if hasattr(message_obj, 'get') else None) or ''
            if not reply:
                reply = getattr(choice, 'text', '') or ''

        return jsonify({'reply': reply.strip()})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@app.route('/graph', methods=['GET'])
def graph():
    return serve_html_with_api_key('graph.htm')

@app.route('/geometry', methods=['GET'])
def geometry():
    return serve_html_with_api_key('geometry.htm')

@app.route('/cal', methods=['GET'])
def cal():
    return serve_html_with_api_key('cal.htm')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
