from flask import Flask, request, jsonify, send_file, g, abort, make_response
from werkzeug.utils import secure_filename
from speech2text import WhisperModel
import os
from functools import wraps
import json
from Validator import Validator
from models.entities.User import User
from models.entities.Query import Query
from database import db
from werkzeug.exceptions import Unauthorized
from flask import request
from flask_caching import Cache
from datetime import datetime
from flask_cors import CORS
import pytz

with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

kyrgyzstan_timezone = pytz.timezone('Asia/Bishkek')

app = Flask(__name__)
CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
devices = config.get("devices")
whisper_models = {}
for device in devices:
    whisper_models[device] = WhisperModel(config, device)

db_config = config.get('db_conf')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_config.get('user_name')}:{db_config.get('password')}@localhost:3306/{db_config.get('db_name')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
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
        return f(*args, **kwargs)

    return decorated_function


@app.route('/api/receive_data', methods=['POST'])
@require_auth
def receive_data():
    current_utc_time = datetime.utcnow()
    new_query = Query(user_id=g.user.id, duration=0, date=current_utc_time.replace(tzinfo=pytz.utc).astimezone(kyrgyzstan_timezone))
    try:
        valid_query = Validator(request, config)
        if valid_query.validate():
            print(valid_query.get_audio_file())
            text = whisper_models[g.user.device].generate_text_from_audio(valid_query.get_audio_file())
            new_query.duration = valid_query.get_duration()
            new_query.status = config.get('SUCCESS_STATUS')
            db.session.add(new_query)
            db.session.commit()
            response_data = {"text": text}

            response = make_response(jsonify(response_data), 200)
            return response
        else:
            response = make_response(jsonify({"error": valid_query.get_error_message()}), 401)
            return response
    except Exception as e:
        error_message = str(e)
        new_query.error_message = error_message
        new_query.status = config.get('ERROR_STATUS')
        db.session.add(new_query)
        db.session.commit()
        response = make_response(jsonify({"error": error_message}), 500)
        return response

        
@app.route('/check_cache')
def check_cache():
    all_keys = cache.cache._cache.keys()
    cache_values = [key for key in all_keys]

    return jsonify(cache_values)


@app.route('/')
def index():
    return "Welcome to Whisper's API"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
