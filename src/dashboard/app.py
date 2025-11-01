"""Flask web dashboard for chat review and manual control"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from functools import wraps
from pathlib import Path
from src.config import Config
from src.storage.database import ChatDatabase
from src.ai.chat_style import ChatStyle


app = Flask(__name__)
app.config['SECRET_KEY'] = Config.DASHBOARD_SECRET_KEY
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database
database = ChatDatabase(Config.DATABASE_PATH, Config.ENCRYPTION_KEY)
chat_style = ChatStyle(Config.CHAT_STYLE_PATH)


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == Config.DASHBOARD_USERNAME and password == Config.DASHBOARD_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/api/conversations')
@login_required
def get_conversations():
    """Get all conversations"""
    try:
        conversations = database.get_all_conversations(limit_per_contact=50)
        return jsonify({
            'success': True,
            'conversations': conversations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/conversation/<contact>')
@login_required
def get_conversation(contact):
    """Get conversation with specific contact"""
    try:
        messages = database.get_conversation(contact, limit=100)
        return jsonify({
            'success': True,
            'contact': contact,
            'messages': messages
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/contacts')
@login_required
def get_contacts():
    """Get approved contacts"""
    try:
        contacts = database.get_approved_contacts()
        return jsonify({
            'success': True,
            'contacts': contacts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/style', methods=['GET'])
@login_required
def get_style():
    """Get current chat style"""
    try:
        return jsonify({
            'success': True,
            'style': chat_style.style_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/style', methods=['POST'])
@login_required
def update_style():
    """Update chat style"""
    try:
        updates = request.json
        chat_style.update_style(updates)
        
        return jsonify({
            'success': True,
            'message': 'Style updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/style/example', methods=['POST'])
@login_required
def add_example():
    """Add example conversation to style"""
    try:
        data = request.json
        context = data.get('context', '')
        response = data.get('response', '')
        
        if not context or not response:
            return jsonify({
                'success': False,
                'error': 'Context and response are required'
            }), 400
        
        chat_style.add_example_conversation(context, response)
        
        return jsonify({
            'success': True,
            'message': 'Example added successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config')
@login_required
def get_config():
    """Get current configuration"""
    return jsonify({
        'success': True,
        'config': {
            'auto_reply_enabled': Config.AUTO_REPLY_ENABLED,
            'ai_provider': Config.AI_PROVIDER,
            'check_interval': Config.CHECK_INTERVAL_SECONDS,
            'max_response_length': Config.MAX_RESPONSE_LENGTH
        }
    })


# WebSocket events for real-time updates
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status', {'message': 'Connected to dashboard'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


def run_dashboard(host=None, port=None):
    """Run the dashboard server
    
    Args:
        host: Host address (default from config)
        port: Port number (default from config)
    """
    host = host or Config.DASHBOARD_HOST
    port = port or Config.DASHBOARD_PORT
    
    print(f"Starting dashboard on http://{host}:{port}")
    print(f"Login with username: {Config.DASHBOARD_USERNAME}")
    
    socketio.run(app, host=host, port=port, debug=False)


if __name__ == '__main__':
    run_dashboard()
