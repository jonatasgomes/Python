from pathlib import Path
from openai import OpenAI
import env

client = OpenAI(api_key=env.OPENAI_API_KEY)
input_text_path = Path(__file__).parent.parent / 'Generate_Text/output.txt'
with open(input_text_path, 'r', encoding='utf-8') as file:
    input_text = file.read().strip()
output_file_path = Path(__file__).parent / 'output.mp3'
response = client.audio.speech.create(
    model='tts-1',
    voice='onyx',
    input=input_text
)

response.stream_to_file('output.mp3')
print('Finished.')
