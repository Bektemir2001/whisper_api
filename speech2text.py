from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio
import torch


class WhisperModel:
    def __init__(self, config, device):
        self.device = "cuda:" + str(device)
        self.model = WhisperForConditionalGeneration.from_pretrained(config.get("model_path")).to(device)
        self.processor = WhisperProcessor.from_pretrained(config.get("processor_path"))

    def generate_text_from_audio(self, audio_file_path):
        audio_input, _ = torchaudio.load(audio_file_path)  # Загрузка файла
        if audio_input.shape[0] == 2:
            audio_input = audio_input.mean(dim=0, keepdim=True)

        inputs = self.processor(audio_input.numpy(), return_tensors="pt", sampling_rate=16000)
        for key in inputs:
            inputs[key] = inputs[key].to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs)

        generated_text = self.processor.decode(outputs[0].to(self.device), skip_special_tokens=True)
        return generated_text

 

