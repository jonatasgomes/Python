from sentence_transformers import SentenceTransformer

def get_embedding(text):
    """
    Get the embedding of a given text using the SentenceTransformer model.
    """
    return model.encode(text, convert_to_tensor=False).tolist()

model = SentenceTransformer('all-MiniLM-L6-v2')
print(get_embedding("a"))
