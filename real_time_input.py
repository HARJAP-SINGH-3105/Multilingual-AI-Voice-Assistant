import whisper
import speech_recognition as sr
model = whisper.load_model("small")
import os
recognizer = sr.Recognizer()
def audio_input():

    with sr.Microphone() as source:
        print("Please speak...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen( source,timeout=15) 

        print("Processing...")
        os.makedirs("temp_audio", exist_ok=True)
        file_path = os.path.join("temp_audio", "audio_input.wav")
        # Save as temporary file
        with open(file_path, "wb") as f:
            f.write(audio.get_wav_data())

        # Transcribe and translate
        # Load audio and detect language
        audio = whisper.load_audio(file_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        # print(probs)
        # # Output most likely language
        # print(f"Detected language: {max(probs, key=probs.get)}")
        result = model.transcribe(file_path, task="translate")
        # print("English Translation:", result["text"])

        return max(probs, key=probs.get), result["text"]

# if __name__=="__main__":
#     lang, text = give_input()
#     print(lang, text)
