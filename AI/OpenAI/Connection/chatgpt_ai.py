from openai import OpenAI
import env

client = OpenAI(api_key=env.OPENAI_API_KEY)

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)

# https://platform.openai.com/docs/guides/text-to-speech