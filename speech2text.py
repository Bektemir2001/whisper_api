from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio
import torch



class WhisperModel:
    def __init__(self, model_path="/Users/aidaizhusup/check_whisper/all-streaming-whisper-small-ky/checkpoint-4000", processor_path="/Users/aidaizhusup/check_whisper/all-streaming-whisper-small-ky"):
        self.model = WhisperForConditionalGeneration.from_pretrained(model_path)
        self.processor = WhisperProcessor.from_pretrained(processor_path)

    def generate_text_from_audio(self, audio_file_path):
    
        audio_input, _ = torchaudio.load(audio_file_path)

        if audio_input.shape[0] == 2:
            audio_input = audio_input.mean(dim=0, keepdim=True)

        inputs = self.processor(audio_input.numpy(), return_tensors="pt", sampling_rate=16000)
        for key in inputs:
            inputs[key] = inputs[key]
        with torch.no_grad():
            outputs = self.model.generate(**inputs)

        generated_text = self.processor.decode(outputs[0], skip_special_tokens=True)
        print(generated_text)
        return generated_text
        

# Example usage:
if __name__ == "__main__":
    whisper_model = WhisperModel()
#    generated_text = whisper_model.generate_text_from_audio("/Users/aidaizhusup/check_whisper/CHECK/n1.wav")
#    print(generated_text)
 

