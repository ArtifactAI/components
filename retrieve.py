from openai import OpenAI
from keys import OPENAI_API_KEY
import chromadb

# Function to generate embeddings using OpenAI's Embedding API
def generate_embedding(text):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def retrieve_similar_files(query, collection, top_k=5):
    # Generate embedding for the query
    query_embedding = generate_embedding(query)
    
    # Search for similar vectors in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=['metadatas', 'distances']
    )
    
    # Return the file paths and their similarity scores
    return list(zip(results['ids'][0], results['distances'][0], results['metadatas'][0]))

if __name__ == "__main__":
    # Initialize ChromaDB with persistent storage
    client = chromadb.PersistentClient(path="./db")
    
    # Create or get the collection
    collection = client.get_or_create_collection("code-embeddings")
    
    query = "can you write a simulation of an airplane?"
    # Retrieve similar files
    similar_files = retrieve_similar_files(query, collection)
    print(similar_files)
