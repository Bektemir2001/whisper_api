from flask import Flask, request, jsonify,send_file,g
from werkzeug.utils import secure_filename
from speech2text import WhisperModel
import os
from pydub import AudioSegment
import json
from Validator import Validator
from models.entities.User import User
from models.entities.Query import Query
from models.entities.SuccessfulQuery import SuccessfulQuery
from database import db
from werkzeug.exceptions import Unauthorized
from flask import request
from flask_caching import Cache
from datetime import datetime

import pytz
kyrgyzstan_timezone = pytz.timezone('Asia/Bishkek')

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

whisper_model = WhisperModel()

# Configure upload folder
UPLOAD_FOLDER = '/Users/aidaizhusup/check_whisper/CHECK'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'aac', 'm4a'} # Allowed file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

db_config = config.get('db_conf')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_config.get('user_name')}:{db_config.get('password')}@localhost:3306/{db_config.get('db_name')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def auth():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        raise Unauthorized('Invalid token')

    token = token[len('Bearer '):]
    user = cache.get(token)
    if user is None:
        user = User.query.filter(User.token == token).first()
        if user is not None:
            cache.set(token, user)

    if user is None:
        raise Unauthorized('Incorrect token')
    if not user.has_access:
        raise Unauthorized('Unauthorized')
    g.user = user


@app.before_request
def before_request():
    return auth()# Function to check if file extension is allowed
    
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_wav(input_file, output_file):
    # Load audio file using pydub
    audio = AudioSegment.from_file(input_file)

    # Ensure the audio is in mono and has a sample rate of 16000 Hz
    audio = audio.set_channels(1).set_frame_rate(16000)

    # Set the bits per sample to 16 bits (2 bytes)
    audio = audio.set_sample_width(2)

    # Convert audio to WAV format
    audio.export(output_file, format="wav")

@app.route('/api/receive_data', methods=['POST'])
def receive_data():
    try:
        duration_limit = 30
        form = Validator(request.files['audio'], duration_limit, g.user)
        current_utc_time = datetime.utcnow()
        new_query = Query(user_id=g.user.id, duration=0, date=current_utc_time.replace(tzinfo=pytz.utc).astimezone(kyrgyzstan_timezone))
        
        
        if 'audio' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['audio']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if not filename.endswith('.wav'):
                wav_filename = os.path.splitext(filename)[0] + '.wav'
                wav_filepath = os.path.join(app.config['UPLOAD_FOLDER'], wav_filename)
                convert_to_wav(filepath, wav_filepath)
                filepath = wav_filepath

            text = whisper_model.generate_text_from_audio(filepath)
            # Создание нового объекта запроса и сохранение в базе данных
            db.session.add(new_query)
            db.session.commit()

            # Создание нового объекта ответа
#            new_response = QueryResponse(query_id=new_query.id, text=text)
#            # Сохранение ответа в базе данных
#            db.session.add(new_response)
#            db.session.commit()

            response_data = {"text": text}
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Invalid file extension"}), 400
    except Exception as e:
        # В случае ошибки сохраняем данные об ошибке в базу данных
        error_message = str(e)
        new_query.error_message = error_message
        db.session.add(new_query)
        db.session.commit()
        return jsonify({"error": error_message}), 500

        
@app.route('/check_cache')
def check_cache():
    all_keys = cache.cache._cache.keys()
    cache_values = [key for key in all_keys]

    return jsonify(cache_values)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7575, debug=True)

