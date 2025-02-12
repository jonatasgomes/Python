from google import genai
import PIL.Image
import os
import env

path = os.path.join(os.path.dirname(__file__), 'Assets/img_02.png')
image = PIL.Image.open(path)

client = genai.Client(api_key=env.GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=['according to this chart give me a high risk high profit strategy for Intel', image]
)

print(response.text)
