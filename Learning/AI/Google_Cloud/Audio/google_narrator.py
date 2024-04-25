from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code="pt-BR",
    name="pt-BR-Neural2-B",
    ssml_gender=texttospeech.SsmlVoiceGender.MALE
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

story_text = "Era uma vez um garoto chamado Marcos, que vivia em um lindo sítio às margens de um grande rio. O sítio tinha muitos animais, mas o preferido de Marcos era Repouso, um cavalo marrom muito tranquilo e amigo."

# Convert to speech
synthesis_input = texttospeech.SynthesisInput(text=story_text)
response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# Save the audio to a file
with open("story.mp3", "wb") as out:
    out.write(response.audio_content)
    print("Audio content written to file 'story.mp3'")
