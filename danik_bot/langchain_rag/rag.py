import pydotenv
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from danik_bot.langchain_rag.retrieval import FAISSRetriever
from danik_bot.langchain_rag.chat import ChatBot

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
            max_new_tokens=300
        )
        self.llm = HuggingFacePipeline(pipeline=pipe)
        # FAISS Retriever
        self.retriever = FAISSRetriever()

        # Safety check prompt
        self.safety_prompt = PromptTemplate(
            input_variables=["query"],
            template=(
                "Определите, является ли следующий запрос безопасным для ответа. "
                "Если запрос безопасен, напишите 'ДА'. Если он небезопасен, напишите 'НЕТ'. "
                "Запрос: {query}. Твой ответ:"
            ),
        )
        self.safety_chain = self.safety_prompt | self.llm

        # Retrieval-based generation prompt
        self.response_prompt = PromptTemplate(
            input_variables=["context", "query"],
            template=(
                "Ты бот казах из Алматы по имени Даник"
                "Используя следующий контекст, ответь на запрос "
                "(Обязательно добавь ссылку 'link'). "
                "Если контекст не содержит информации, "
                "связанной с запросом, скажите: 'Извините, по вашему запросу у меня нет данных'.\n\n"
                "Контекст: {context}\n\nЗапрос: {query} \n\n Ответ:"
            ),
        )
        self.response_chain = self.response_prompt | self.llm

    def process_query(self, query: str):
        """
        Process the user query through the pipeline.
        """
        # Step 1: Safety check
        safety_result = self.safety_chain.invoke({'query': query})
        print(safety_result)
        if safety_result.upper() != "НЕТ":
            return "Извините, этот запрос небезопасен."

        # Step 2: Retrieve top 5 documents
        top_results = self.retriever.retrieve(query)
        if not top_results:
            return "Извините, по вашему запросу у меня нет данных."

        # Combine retrieved results into a single context
        context = "\n".join([
            f'{result.page_content}. Метаданные {result.metadata}'
            for result in top_results
        ])

        # Step 3: Generate response using retrieved context
        response = self.response_chain.invoke({"context": context, "query": query}).strip()
        response = response.replace(self.response_prompt, '')
        return response
c = DanikBotPipeline()
c.process_query('Где поесть вкусный удон?')