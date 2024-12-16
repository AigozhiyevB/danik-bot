import json
from uuid import uuid4

import numpy as np
import faiss
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
import pydotenv
from tqdm import tqdm

# File paths
env = pydotenv.Environment()
jsonl_file = env.get('RAW_DATA')
faiss_index_path = env.get('FAISS_DB')

model = SentenceTransformer(env.get('EMBEDDINGS_MODEL'))  # Use an appropriate model

# Read JSONL file and extract text data
jsons = []
with open(jsonl_file, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        # Assuming the text to embed is in the 'content' field
        jsons.append(data)

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(jsons[0]['text'])

# Convert to numpy array
embeddings = np.array(embeddings, dtype='float32')

# Create FAISS index
print("Creating FAISS index...")
dimension = embeddings.shape[0]
index = faiss.IndexFlatIP(dimension)  # L2 distance
vector_store = FAISS(
    embedding_function=model.encode,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

# Get Documents
documents = []
for i in tqdm(jsons):
    text = f'{i["text"]}. Средний чек: {i["mean_bill"]}. Кухни: {i["kitchens"]}'
    doc = Document(
        page_content=text,
        metadata = {'link': i['link'], 'name': i['name']}
    )
    documents.append(doc)

uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)

# Save vector store
print(f'Saving into {faiss_index_path}')
vector_store.save_local(faiss_index_path)