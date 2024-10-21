import os
import chromadb
from openai import OpenAI

from keys import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Configure the folders to include for embedding
FOLDERS_TO_EMBED = ["mechanics"]

# The file types to embed (you can add more extensions if needed)
ALLOWED_EXTENSIONS = ['.ipynb']  # Only embed these file types

# Function to read a file and return its content
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

# Function to generate embeddings using OpenAI's Embedding API
def generate_embedding(text):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Function to walk through folders and process each file
def process_repository(folders, collection):
    for folder in folders:
        for root, _, files in os.walk(folder):
            for file in files:
                # Check for allowed extensions
                if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    try:
                        file_content = read_file(file_path)
                        print(f"Embedding file: {file_path}")
                        
                        # Generate embedding for the file content
                        embedding = generate_embedding(file_content)
                        
                        # Store embedding in ChromaDB
                        collection.add(
                            documents=[file_content],
                            embeddings=[embedding],
                            metadatas=[{"source": file_path}],
                            ids=[file_path]
                        )
                    except Exception as e:
                        print(f"Failed to process {file_path}: {str(e)}")

# Main execution
if __name__ == "__main__":
    # Initialize ChromaDB with persistent storage
    client = chromadb.PersistentClient(path="./db")
    
    # Create or get the collection
    collection = client.get_or_create_collection("code-embeddings")
    
    # Process the specified folders and store embeddings in ChromaDB
    process_repository(FOLDERS_TO_EMBED, collection)
    
    print("Finished embedding and storing files.")
