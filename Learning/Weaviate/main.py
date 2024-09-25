import weaviate as w
# import weaviate.classes as wvc
import env

client = w.connect_to_wcs(
    cluster_url=env.WEAVIATE_REST_URL,
    auth_credentials=w.auth.AuthApiKey(env.WEAVIATE_API_KEY))

try:
    print(client.is_ready())
    questions = client.collections.get("Questions")
    questions.data.insert_many([{'question': 'Question 1', 'answer': 'Answer 1'}])
finally:
    client.close()
