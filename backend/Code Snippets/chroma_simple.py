import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

EMBED_MODEL = os.getenv("EMBED_MODEL") # ChromaDB by default use all-MiniLM-L6-v2 model for generating embeddings but since i am using OpenAI's API for generating embeddings, i need to specify the model.

#Get the embedding of a text using EMBED_MODEL
def get_embedding(text):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return response.data[0].embedding


chunks = {
    "c0": "Leave Policy - Maternity Leave\nMaternity leave is 26 weeks of paid leave for the first two children.",
    "c1": "Medical Policy - Maternity Cover\nHospitalization for childbirth is covered up to 75,000 rupees.",
    "c2": "Travel Expense - Reimbursement\nSubmit expense claims within 30 days of the trip. Approved claims are reimbursed within 7 working days.",
    "c3": "Tech Docs - Deployment Windows\nProduction deployments are allowed on Tuesdays and Thursdays between 11 AM and 4 PM.",
}

ids = list(chunks.keys())
documents = list(chunks.values())

embeddings = []
for s in documents:
    embedding = get_embedding(s)
    embeddings.append(embedding)

# chroma = chromadb.Client() # this will create a chroma db in memory (deleted once the program ends and then you have to reinitilize)
chroma = chromadb.PersistentClient(path="./chromadbStorage") # this will create a chroma db in the disk (persists even after the program ends)

# zorvex_collection = chroma.create_collection( # this will create a chroma collection if not exists
zorvex_collection = chroma.get_or_create_collection( # this will create a chroma collection if not exists else it will return the existing collection
    name="zorvex_technology",
    configuration={
        "hnsw": {
            "space": "cosine", # cosine similarity is used to find the similarity between the query and the documents instead of Euclidean distance (L2)
        }
    }
)

# zorvex_collection.add( # This will only insert the documents if they don't exist. It will throw an error if the documents already exist.
zorvex_collection.upsert( #It will update if an Id is existing, otherwise it will insert a new record
    ids=ids,
    documents=documents,
    embeddings=embeddings,
)


query = "When is the production deployment allowed ? "
query_embdding = get_embedding(query)

results = zorvex_collection.query(
    query_embeddings=[query_embdding],
    n_results=1
)

print(results["documents"][0])



