import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import socket
import threading
import json
import time
import os
import sys

# Add the src folder to path so db_manager can be found if running from outside
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db_manager import DatabaseManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize Database Manager
db = DatabaseManager()

# Logging Setup
def log_to_file(msg):
    with open("bridge_log.txt", "a") as f:
        f.write(msg + "\n")
    print(msg)

log_to_file("[INIT] Web Bridge Starting...")

# TCP Client Configuration
TCP_HOST = '127.0.0.1'
TCP_PORT = 5555
tcp_client = None

# AI Models
try:
    from gesture_classifier import GestureClassifier
    gesture_classifier = GestureClassifier()
    print("[WEB-BRIDGE] Gesture Model Loaded")
except Exception as e:
    print(f"[WEB-BRIDGE] Failed to load Gesture Model: {e}")
    gesture_classifier = None

try:
    from emotion_detection import EmotionDetector
    emotion_detector = EmotionDetector(mtcnn=False)
    print("[WEB-BRIDGE] Emotion Model Loaded")
except Exception as e:
    print(f"[WEB-BRIDGE] Failed to load Emotion Model: {e}")
    emotion_detector = None

try:
    from gesture_player import GesturePlayer
    # Use existing data path
    gesture_player = GesturePlayer(data_path='data/gesture_data.csv')
    print("[WEB-BRIDGE] Gesture Player Loaded")
except Exception as e:
    print(f"[WEB-BRIDGE] Failed to load Gesture Player: {e}")
    gesture_player = None

try:
    from text_processing import TextProcessor
    text_processor = TextProcessor()
    print("[WEB-BRIDGE] Text Processor Loaded")
except Exception as e:
    print(f"[WEB-BRIDGE] Failed to load Text Processor: {e}")
    text_processor = None

# Buffers
client_gesture_state = {}

# Store messages to show history to new connections
message_history = []

# Map session IDs to their chosen language
client_languages = {}

def send_translated_message(json_data, sid=None):
    """Translates message content to target client's language and emits it."""
    # If a specific sid is provided
    if sid:
        target_lang = client_languages.get(sid, 'English')
        outgoing_data = dict(json_data) # Copy
        if text_processor and outgoing_data.get('type') in ('text', 'speech', 'gesture'):
            outgoing_data['content'] = text_processor.translate_text(outgoing_data['content'], target_lang)
        socketio.emit('new_message', outgoing_data, to=sid)
    else:
        # Broadcast to all clients individually so they get their own language
        # request is not available here, so we iterate through connected clients manually
        # Note: Eventlet provides a way to loop through connected sids via socketio.server.manager.rooms
        # But a simple way is emitting directly mapped to client_languages which we track on connect.
        for client_sid, target_lang in list(client_languages.items()):
            outgoing_data = dict(json_data) # Copy
            if text_processor and outgoing_data.get('type') in ('text', 'speech', 'gesture'):
                outgoing_data['content'] = text_processor.translate_text(outgoing_data['content'], target_lang)
            socketio.emit('new_message', outgoing_data, to=client_sid)


def tcp_listener():
    """Listens for messages from the main TCP server and relays to Web."""
    global tcp_client
    while True:
        try:
            if tcp_client is None:
                tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_client.connect((TCP_HOST, TCP_PORT))
                print(f"[WEB-BRIDGE] Connected to TCP Server at {TCP_HOST}:{TCP_PORT}")
            
            data = tcp_client.recv(4096)
            if not data:
                print("[WEB-BRIDGE] TCP Disconnected. Reconnecting...")
                tcp_client.close()
                tcp_client = None
                time.sleep(2)
                continue
                
            msg = data.decode('utf-8')
            try:
                json_data = json.loads(msg)
                # Relay to Web Clients (translated individually)
                send_translated_message(json_data)
                
                # Check for Avatar Trigger (Text -> Sign)
                if gesture_player and json_data.get('type') == 'text':
                    text_content = json_data.get('content', '').strip()
                    # Try to find a gesture for the last word or whole phrase
                    # Prioritize exact match, then single word
                    gesture_lms = gesture_player.get_gesture_landmarks(text_content)
                    if not gesture_lms:
                        # Try last word
                        words = text_content.split()
                        if words:
                            gesture_lms = gesture_player.get_gesture_landmarks(words[-1])
                    
                    if gesture_lms:
                        print(f"[WEB-BRIDGE] Sending Avatar Gesture: {text_content}")
                        socketio.emit('avatar_frame', {'landmarks': gesture_lms, 'gesture': text_content})
                
                # Add to history
                if json_data not in message_history:
                     message_history.append(json_data)
                     if len(message_history) > 50: message_history.pop(0)
                     
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            print(f"[WEB-BRIDGE] TCP Error: {e}")
            if tcp_client:
                try: tcp_client.close() 
                except: pass
            tcp_client = None
            time.sleep(2)

def process_gesture_data(landmarks, sid):
    """
    landmarks: list of 42 (x,y,z) points (21 left + 21 right from FrontEnd)
    """
    global client_gesture_state
    
    if not gesture_classifier: return None
    
    if sid not in client_gesture_state:
        client_gesture_state[sid] = {'buffer': [], 'last_sent': None}
        
    state = client_gesture_state[sid]
    
    # If all zeros (no hands), clear buffer and return
    if not landmarks or (max(landmarks) == 0.0 and min(landmarks) == 0.0):
        state['buffer'].clear()
        state['last_sent'] = None
        return None
        
    features = landmarks
    
    # Log feature stats
    log_to_file(f"[PREDICT] Features: Min={min(features):.2f}, Max={max(features):.2f}, Mean={sum(features)/len(features):.2f}")

    # Ask AI for Top 5 predictions
    top_preds = gesture_classifier.predict_top_n_gestures(features, n=5)
    
    if not top_preds:
        return None
        
    # top_preds is a list of (gesture, confidence) tuples.
    # We use the top-1 gesture for stability buffering
    top_gesture, conf = top_preds[0]

    state['buffer'].append(top_gesture)
    if len(state['buffer']) > 10: state['buffer'].pop(0) # Length 10 for stability
    
    from collections import Counter
    most_common, count = Counter(state['buffer']).most_common(1)[0]
    
    # Trigger when gesture is stable (count > 8)
    if count > 8:
        if most_common != state['last_sent']:
            state['last_sent'] = most_common
            print(f"[WEB-BRIDGE] STABLE GESTURE: {most_common}")
            
            # Extract just the string words from the top predictions
            suggested_words = [p[0] for p in top_preds]
            return suggested_words
            
    return None


# Start TCP Listener in background thread
eventlet.spawn(tcp_listener)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    client_languages[sid] = 'English' # Default
    print(f'[WEB] Client connected: {sid}')
    log_to_file(f"[WEB] Client connected: {sid}")
    # Send history (translated individually)
    for msg in message_history:
        send_translated_message(msg, sid=sid)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in client_languages:
        del client_languages[sid]
    if sid in client_gesture_state:
        del client_gesture_state[sid]

@socketio.on('web_login')
def handle_web_login(data):
    username = data.get('username')
    password = data.get('password')
    sid = request.sid
    print(f"[WEB] Login attempt from {username} ({sid})")
    
    success, message, user_type = db.validate_user(username, password)
    
    if success:
        print(f"[WEB] {username} logged in successfully as {user_type}.")
        
        # Get Gesture Vocabulary for Suggestions
        vocab = []
        if gesture_classifier and gesture_classifier.model:
            vocab = [str(c) for c in gesture_classifier.model.classes_ if len(str(c)) > 1 and str(c) not in ("NEXT", "SPACE")]
            
        emit('login_response', {
            'success': True,
            'message': message,
            'username': username,
            'user_type': user_type,
            'vocabulary': vocab
        })
    else:
        print(f"[WEB] Failed login for {username}: {message}")
        emit('login_response', {
            'success': False,
            'message': message
        })
        
@socketio.on('set_language')
def handle_set_language(data):
    sid = request.sid
    lang = data.get('lang', 'English')
    client_languages[sid] = lang
    print(f"[WEB] Client {sid} set language to {lang}")

@socketio.on('send_message')
def handle_send_message(data):
    """
    data: {'sender': 'WebUser', 'content': 'Hello', 'type': 'text'}
    """
    print(f"[WEB] Received: {data}")
    # Relay to TCP Server
    if tcp_client:
        try:
            # Ensure format matches main app expectation
            if 'emotion' not in data: data['emotion'] = 'Neutral'
            if 'type' not in data: data['type'] = 'text'
            
            msg_str = json.dumps(data)
            tcp_client.send(msg_str.encode('utf-8'))
            
            # Echo to all web clients with translations
            send_translated_message(data)
            
            if data not in message_history:
                 message_history.append(data)
            
        except Exception as e:
            print(f"[WEB-BRIDGE] Send Error: {e}")
# ... (Inside socketio handler)

@socketio.on('process_frame')
def handle_process_frame(data):
    """
    data: {
        'landmarks': [float, ...], # 126 floats
        'message_part': bool 
    }
    """
    try:
        # print(".", end="", flush=True) # Heartbeat for frame RX
        landmarks = data.get('landmarks', [])
        sid = request.sid
        if len(landmarks) == 126:
            result = process_gesture_data(landmarks, sid)
            if result:
                # 1. Feedback to Web User ONLY
                # Web Client is now responsible for building sentences from suggestions
                emit('gesture_detected', {'suggestions': result})
                
    except Exception as e:
        print(f"[WEB-BRIDGE] Frame Error: {e}")

@socketio.on('process_emotion')
def handle_process_emotion(data):
    try:
        landmarks = data.get('face_landmarks', [])
        w = data.get('width', 640)
        h = data.get('height', 480)
        if len(landmarks) >= 1404 and emotion_detector:
            emotion, score = emotion_detector.detect_emotion_from_landmarks(landmarks, w, h)
            emit('emotion_detected', {'emotion': emotion, 'score': score})
    except Exception as e:
        print(f"[WEB-BRIDGE] Emotion Error: {e}")

@socketio.on('clear_gesture_buffer')
def handle_clear_gesture():
    sid = request.sid
    if sid in client_gesture_state:
        client_gesture_state[sid]['buffer'].clear()
        client_gesture_state[sid]['last_sent'] = None
    print(f"[WEB-BRIDGE] Client {sid} cleared gesture buffer")


def generate_self_signed_cert():
    """Generates a self-signed certificate for HTTPS."""
    try:
        from OpenSSL import crypto
    except ImportError as e:
        print(f"[WEB-BRIDGE] pyopenssl import failed: {e}")
        log_to_file(f"[WEB-BRIDGE] pyopenssl import failed: {e}")
        return None, None

    if os.path.exists("cert.pem") and os.path.exists("key.pem"):
        return "cert.pem", "key.pem"

    print("[WEB-BRIDGE] Generating self-signed certificate...")
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "State"
    cert.get_subject().L = "City"
    cert.get_subject().O = "Organization"
    cert.get_subject().OU = "Organizational Unit"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    with open("cert.pem", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open("key.pem", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    return "cert.pem", "key.pem"

if __name__ == '__main__':
    # Listen on 0.0.0.0 to allow external connections
    cert, key = generate_self_signed_cert()
    if cert and key:
        msg = f"[WEB-BRIDGE] Starting Web Server on HTTPS (0.0.0.0:5000)"
        print(msg)
        log_to_file(msg)
        
        # Get Local IP and Hostname
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            hostname = socket.gethostname()
            
            print(f"\n{'='*60}")
            print(f" OPTION 1 (Best): Connect using HOSTNAME (No IP needed):")
            print(f"   https://{hostname}:5000")
            print(f"   (If that fails, use IP below)")
            print(f" OPTION 2: Connect using IP Address:")
            print(f"   https://{local_ip}:5000")
            print(f"{'='*60}\n")
        except:
            print("\n[INFO] Could not determine local IP. Check ipconfig.\n")

        try:
            socketio.run(app, host='0.0.0.0', port=5000, certfile=cert, keyfile=key)
        except Exception as e:
            log_to_file(f"[FATAL] HTTPS Start Failed: {e}")
    else:
        msg = f"[WEB-BRIDGE] Starting Web Server on HTTP (0.0.0.0:5000) - Camera might fail remotely"
        print(msg)
        log_to_file(msg)
        socketio.run(app, host='0.0.0.0', port=5000)
