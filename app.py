import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    """Basic hello endpoint"""
    return jsonify({
        'message': 'Hello from Flask on Cloud Run!',
        'status': 'ok'
    })


@app.route('/health')
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    # Cloud Run will set the PORT environment variable
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
