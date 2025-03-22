import os
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import TFIDFRetriever
from langchain_huggingface import HuggingFaceEmbeddings
import pydotenv

# Load environment variables
env = pydotenv.Environment()

FAISS_INDEX_PATH = env.get("FAISS_DB")  # Path to FAISS index
EMBEDDINGS_MODEL_PATH = env.get("EMBEDDINGS_MODEL")  # HuggingFace embeddings model


class FAISSRetriever:
    def __init__(self):
        # Load the embeddings model
        self.embeddings_model = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_PATH)

        # Load FAISS index
        if not os.path.exists(FAISS_INDEX_PATH):
            raise FileNotFoundError(f"FAISS index not found at {FAISS_INDEX_PATH}")
        self.index = FAISS.load_local(
            FAISS_INDEX_PATH,
            self.embeddings_model,
            allow_dangerous_deserialization=True
        )


    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve top-k similar documents using FAISS.
        """
        indices = self.index.search(query, 'similarity', k=top_k)

        # Filter results where distance is valid (ensure FAISS returns valid results)
        results = [
            idx
            for idx in indices
            if idx != -1  # Ensure FAISS index is valid
        ]
        return results


class MyTFIDF:
    def __init__(self):
        path = env.get('TF_IDF')
        self._retriever = TFIDFRetriever.load_local(path, allow_dangerous_deserialization=True)

    def retrieve(self, query: str):
        return self._retriever.invoke(query)