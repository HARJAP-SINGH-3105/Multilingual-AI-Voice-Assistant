import os
from gtts import gTTS
from googletrans import Translator
from pydub import AudioSegment
from pydub.playback import play
import asyncio


def audio_output(response,lang):
  # Step 1: Translate to desired language
  async def TranslateText():
    async with Translator() as translator:
      result = await translator.translate(response, src="en", dest=lang)
      return result.text

  translated_text = asyncio.run(TranslateText())
  # print(translated_text)

  # Step 2: Save to temp file
  temp_dir = os.path.join(os.getcwd(), "temp_audio")
  os.makedirs(temp_dir, exist_ok=True)
  file_path = os.path.join(temp_dir, "audio_output.mp3")

  # Step 3: Convert text to speech and save
  tts = gTTS(translated_text, lang= lang)
  tts.save(file_path)
  # return file_path
 # play audio
  # print("Listen the response.........")
  audio = AudioSegment.from_mp3(file_path)
  play(audio)
