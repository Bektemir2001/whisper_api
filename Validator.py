from mutagen.mp3 import MP3
import os


class Validator:
    error_message = ''
    audio = None
    duration_limit = 0
    file_path = ''
    duration = 0

    def __init__(self, request, config):
        self.request = request
        self.duration_limit = config.get("DURATION_LIMIT")
        self.config = config

    def validate(self):

        if 'audio' not in self.request.files:
            self.error_message = f'No audio file provided.'
            return False

        self.audio = self.request.files['audio']
        if self.audio.filename.split('.')[-1].lower() != 'mp3':
            self.error_message = f'The file must be in MP3 format.'
            return False

        self.file_path = self.config.get('UPLOAD_FOLDER') + "/" + self.audio.filename
        self.audio.save(self.file_path)
        audio_file = MP3(self.file_path)
        self.duration = audio_file.info.length

        if self.duration > self.duration_limit:
            self.error_message = f'The audio file must not exceed {self.duration_limit} seconds. Your audio file {self.duration} seconds'
            os.remove(self.file_path)
            return False
        return True

    def get_error_message(self):
        return self.error_message
    
    def get_audio_file(self):
        return self.file_path
    def get_duration(self):
        return self.duration
