from openai import OpenAI
import env

def write_to_file(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)

client = OpenAI(api_key=env.OPENAI_API_KEY)
completion = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "Você é um escritor brasileiro de histórias infantis"},
        {"role": "user",
         "content": "Escreva uma estoria curta com um garoto chamado Lucas que tem um cachorro Totó. Sobre brincar na areia da praia."}
    ]
)

write_to_file(completion.choices[0].message.content, "output.txt")
print('done.')
