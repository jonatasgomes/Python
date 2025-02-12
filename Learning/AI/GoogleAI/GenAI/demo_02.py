import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Optional
import os
import env

path = os.path.join(os.path.dirname(__file__), 'Assets/img_02.png')

class Company(BaseModel):
  name: str
  public: bool
  symbol: Optional[str]
  long: Optional[bool]

class Theme(BaseModel):
  name: str

client = genai.Client(api_key=env.GEMINI_API_KEY)
model = "gemini-2.0-flash"
path = os.path.join(os.path.dirname(__file__), 'Assets/pdf_01.pdf')
file_ref = client.files.upload(file=path)

extract_themes_prompt = """Attached is a list of IPO forecast for 2025. Analyze it and extract all of the names dicussed."""
print(client.models.count_tokens(model=model, contents=[extract_themes_prompt, file_ref]))
result = client.models.generate_content(
  model=model,
  contents=[file_ref, extract_themes_prompt],
  config=types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=list[Theme]
  ),
)

print(result)
