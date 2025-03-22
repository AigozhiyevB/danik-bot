import json
from uuid import uuid4

from langchain_community.retrievers import TFIDFRetriever
from langchain_core.documents import Document
import pydotenv
from tqdm import tqdm

# File paths
env = pydotenv.Environment()
jsonl_file = env.get('RAW_DATA')
faiss_index_path = env.get('FAISS_DB')
tf_idf_path = env.get('TF_IDF')

if __name__ == '__main__':
    jsons = []
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            # Assuming the text to embed is in the 'content' field
            jsons.append(data)

    docs = []
    for i in tqdm(jsons):
        i['id'] = uuid4()
        content = i.pop('text')
        docs.append(Document(page_content=content, metadata=i))

    retriever = TFIDFRetriever.from_documents(docs)
    result = retriever.invoke("Где поесть суши")
    retriever.save_local(tf_idf_path)
