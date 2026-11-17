import json
import os

# import numpy
# from openai import OpenAI  # <-- [PREVIOUS]: Used OpenAI client to request embeddings from Ollama / remote API
from sentence_transformers import SentenceTransformer  # <-- [NEW]: Loads and runs embedding model directly in Python
from dotenv import load_dotenv
import chromadb

load_dotenv() #by default looks for .env file

# --- [PREVIOUS]: Client setup for Ollama embeddings ---
# client = OpenAI(
#     base_url=os.getenv("BASE_URL"),
#     api_key=os.getenv("API_KEY")
# )
# EMBED_MODEL       = os.getenv("EMBED_MODEL")

# --- [NEW]: Initialize SentenceTransformer model directly in-memory ---
EMBED_MODEL_NAME  = os.getenv("EMBED_MODEL", "nomic-ai/nomic-embed-text-v1.5")
embedding_model   = SentenceTransformer(EMBED_MODEL_NAME, trust_remote_code=True)

KB_FOLDER         = os.getenv("KB_FOLDER")
VECTOR_STORE_FILE = os.getenv("VECTOR_STORE_FILE")


# Creates a persistent Chroma database folder on disk
chroma_client = chromadb.PersistentClient(path="./chromadbStorage")

# Create or fetch collection using cosine similarity
collection = chroma_client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}
)




# --- [PREVIOUS]: Calling embeddings via OpenAI API protocol ---
# def get_embedding(text):
#     response = client.embeddings.create(
#         model=EMBED_MODEL,
#         input=text
#     )
#     return response.data[0].embedding

# --- [NEW]: Computing embeddings locally via sentence-transformers ---
# Get the embedding of a text from Embedding model
def get_embedding(text):
    return embedding_model.encode(text).tolist()

# ---[Previous]--- Before integrating ChromaDB
#Get the cosine similarity between two vectors
# def cosine_similarity(A, B):
#     dot_prod = numpy.dot(A, B)
#     norm_a = numpy.linalg.norm(A)
#     norm_b = numpy.linalg.norm(B)
#     return dot_prod / (norm_a * norm_b)

#Load the documents
def load_documents(folder=KB_FOLDER):
    documents = []
    
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            documents.append(
                {
                    "source": filename,
                    "text":f.read(),
                }
            )
        
    return documents

#Add embeddings in the chunks
def add_embeddings(chunks):
    for chunk in chunks:
        vector = get_embedding(chunk["text"])
        chunk["vector"] = vector
    
    return chunks
    
# Takes one file and create multiple chunks from it. One Section = One Chunk
def chunk_document(document):
    chunks = []

    chunk_id = 0
    for part in document["text"].split("\n\n"):
        part = part.strip()
        if part:
            chunks.append(
                {
                    "source": document["source"],
                    "chunk_id": chunk_id,
                    "text": part,
                }
            )
            chunk_id += 1
    
    return chunks

#loads the knowledge base and create chunks from each document
def create_chunks():
    documents = load_documents()
    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))

    return chunks


def index_documents():
    # Only index if ChromaDB is currently empty
    if collection.count() == 0:
        chunks = create_chunks()  # Uses your existing chunking logic
        
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:
            chunk_id = f"{chunk['source']}#{chunk['chunk_id']}"
            vector = get_embedding(chunk["text"])

            ids.append(chunk_id)
            documents.append(chunk["text"])
            embeddings.append(vector)
            metadatas.append({
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"]
            })

        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"ChromaDB: Indexed {len(ids)} chunks into persistent storage.")
    else:
        print(f"ChromaDB: Loaded {collection.count()} existing chunks from disk.")
# ---[Previous]--- Before integrating ChromaDB
# def save_vector_store(chunks):
#     with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as f:
#         json.dump(chunks, f, indent=4)




# ---[Previous]--- Before integrating ChromaDB
# def load_vector_store():
#     with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
#         return json.load(f) #returns the chunks

# def load_chunks():
#     if os.path.exists(VECTOR_STORE_FILE):
#         chunks = load_vector_store()
#         print(f"Loaded {len(chunks)} chunks from the {VECTOR_STORE_FILE}")
#     else:
#         chunks = create_chunks()
#         chunks = add_embeddings(chunks)
#         save_vector_store(chunks)
#         print(f"Created and embedded {len(chunks)} chunks and saved to {VECTOR_STORE_FILE}")

#     return chunks

# chunks = load_chunks()
# --- [NEW: Populate & Load ChromaDB on startup] ---
index_documents()

#Search method to search the top_k chunks for a user_query
def search(query, top_k=3):
    # --- [NEW: Handle empty collection]
    #If your knowledge base has fewer chunks than top_k (for example, you only have 2 chunks, but top_k=3),
    # ChromaDB can raise a warning. Adding a check for collection.count() avoids this:
    if collection.count() == 0:
        return []
    actual_k = min(top_k, collection.count())
    query_vector = get_embedding(query)
    query_results = collection.query(
        query_embeddings=[query_vector],
        n_results=actual_k
    )

    # --- [PREVIOUS]: Calling embeddings via OpenAI API protocol ---
    query_vector = get_embedding(query)

    query_results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )

    # Transform ChromaDB's output back to the format tools.py expects:
    results = []
    num_results = len(query_results["ids"][0])
    for i in range(num_results):
        metadata = query_results["metadatas"][0][i]
        document_text = query_results["documents"][0][i]
        # In cosine distance: similarity = 1 - distance
        distance = query_results["distances"][0][i]
        similarity_score = 1.0 - distance

        results.append({
            "source": metadata["source"],
            "chunk_id": metadata["chunk_id"],
            "text": document_text,
            "score": similarity_score,
            "size": len(document_text)
        })

    return results
# ---[Previous]--- Before integrating ChromaDB
# def search(query, top_k=3):
#     query_vector = get_embedding(query)

#     results = []
#     for chunk in chunks:
#         score = cosine_similarity(query_vector, chunk["vector"])
#         results.append(
#             {
#                 "score" : float(score),
#                 "source": chunk["source"],
#                 "chunk_id": chunk["chunk_id"],
#                 "text": chunk["text"],
#                 "size": len(chunk["text"])
#             }
#         )

#     results.sort(key=lambda rec: rec["score"], reverse=True)
#     return results[:top_k]