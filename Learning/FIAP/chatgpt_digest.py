from openai import OpenAI
import env

def write_to_file(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)

client = OpenAI(api_key=env.OPENAI_API_KEY)

assistant = client.beta.assistants.create(
    name="WhatsApp Chat Digest Assistant",
    instructions="You are an expert WhatsApp chat figest. Use you knowledge base to create a digest about an exported chat file.",
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}],
)

vector_store = client.beta.vector_stores.create(name="WhatsApp Digest")

file_paths = ["./whatsapp_chat.txt"]
file_streams = [open(path, "rb") for path in file_paths]
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)
print(file_batch.status)
print(file_batch.file_counts)

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Create a disgest of the attached WhatsApp chat file. Do it in Brazilian Portuguese. Do not translate any text that is in English.",
        }
    ]
)
print(thread.tool_resources.file_search)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)
messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
message_content = messages[0].content[0].text
annotations = message_content.annotations
citations = []
for index, annotation in enumerate(annotations):
    message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
    if file_citation := getattr(annotation, "file_citation", None):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f"[{index}] {cited_file.filename}")

print(message_content.value)
write_to_file(message_content.value, "whatsapp_digest.txt")
