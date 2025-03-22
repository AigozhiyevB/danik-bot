import pydotenv
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from prompts import SAFETY_PROMPT, RESPONSE_PROMPT
from retrieval import MyTFIDF
from chat import ChatBot

# Load environment variables
env = pydotenv.Environment()

CHAT_MODEL_PATH = env.get("CHAT_MODEL")  # HuggingFace chat model
EMBEDDINGS_MODEL_PATH = env.get("EMBEDDINGS_MODEL")  # HuggingFace embeddings model


class DanikBotPipeline:
    def __init__(self):
        # Load models
        bot = ChatBot()
        pipe = pipeline(
            'text-generation',
            model = bot.model,
            tokenizer=bot.tokenizer,
            max_new_tokens=1000
        )
        self.llm = HuggingFacePipeline(pipeline=pipe)
        # FAISS Retriever
        self.retriever = MyTFIDF()

        # Safety check prompt
        self.safety_prompt = SAFETY_PROMPT
        self.safety_chain = self.safety_prompt | self.llm.bind(skip_prompt=True, max_length=12)


    @property
    def response_chain(self):
        return RESPONSE_PROMPT | self.llm.bind(skip_prompt=True)


    def process_query(self, query: str):
        """
        Process the user query through the pipeline.
        """

        # Step 1: Retrieve top 5 documents
        top_results = self.retriever.retrieve(query)
        if not top_results:
            return "Извините, по вашему запросу у меня нет данных."

        # Combine retrieved results into a single context
        context = "\n".join([
            f'{result.page_content}. Метаданные {result.metadata}'
            for result in top_results
        ])

        # Step 2: Generate response using retrieved context
        response = self.response_chain.invoke({"context": context, "query": query}).strip()
        return response
