import openai
import openai_config

openai.api_key = openai_config.API_KEY

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Translate the following English text to French: 'Hello, how are you?'",
  max_tokens=60
)

print(response.choices[0].text.strip())
