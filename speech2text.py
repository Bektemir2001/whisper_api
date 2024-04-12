from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio
import torch


class WhisperModel:
    def __init__(self, config, device):
        self.device = "cuda:" + str(device)
        self.model = WhisperForConditionalGeneration.from_pretrained(config.get("model_path")).to(device)
        self.processor = WhisperProcessor.from_pretrained(config.get("processor_path"))
        self.config = config

    def generate_text_from_audio(self, audio_file_path):
        wav_file_path = self.config.get('UPLOAD_FOLDER') + "/" + str(randint(1000000, 9999999)) + "#"
        wav_file_path += str(randint(1000000, 9999999)) + ".wav"
        self.convert_to_wav(audio_file_path, wav_file_path)
        audio_input, _ = torchaudio.load(wav_file_name)
        if audio_input.shape[0] == 2:
            audio_input = audio_input.mean(dim=0, keepdim=True)

        inputs = self.processor(audio_input.numpy(), return_tensors="pt", sampling_rate=16000)
        for key in inputs:
            inputs[key] = inputs[key].to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs)

        generated_text = self.processor.decode(outputs[0].to(self.device), skip_special_tokens=True)
        os.remove(wav_file_path)
        os.remove(audio_file_path)
        return generated_text

    @staticmethod
    def convert_to_wav(input_file, output_file):
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio = audio.set_sample_width(2)
        audio.export(output_file, format="wav")
