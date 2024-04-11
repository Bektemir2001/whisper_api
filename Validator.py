class Validator:
    error_message = ''
    audio_file = ''
    duration_limit = 0
    
    def __init__(self, request, audio_file, duration_limit):
        self.request = request
        self.audio_file = audio_file
        self.duration_limit = duration_limit
   
        
    def validate(self):
        if not self.request.is_json:
            self.error_message = 'Invalid JSON request'
            return False
        # Проверка наличия аудиофайла
        if not self.audio_file:
            self.error_message = 'No audio file provided.'
            return False
        
        # Проверка формата аудиофайла (может потребоваться добавить поддержку других форматов)
        supported_formats = ['.wav', '.mp3']
        if not any(self.audio_file.endswith(format) for format in supported_formats):
            self.error_message = f'Unsupported audio format. Supported formats are: {", ".join(supported_formats)}'
            return False
        
        # Проверка длительности аудиофайла
        audio_duration = self.get_audio_duration()
        if audio_duration > self.duration_limit:
            self.error_message = f'Audio duration exceeds the limit of {self.duration_limit} seconds.'
            return False
        
        # Дополнительные проверки, если необходимо
        
        # Если все проверки пройдены успешно, возвращаем True
        return True
    
    def get_error_message(self):
        return self.error_message
    
    def get_audio_file(self):
        return self.audio_file
    
    def get_audio_duration(self):
        # Здесь можно использовать библиотеку для работы с аудиофайлами, чтобы получить его длительность
        # Например, для файлов в формате WAV:
        import wave
        with wave.open(self.audio_file, 'rb') as audio:
            frames = audio.getnframes()
            rate = audio.getframerate()
            duration = frames / float(rate)
        return duration
