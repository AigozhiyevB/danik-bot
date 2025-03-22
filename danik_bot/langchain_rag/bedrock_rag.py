import os
import pydotenv
from langchain_aws import ChatBedrock
from prompts import SAFETY_PROMPT, RESPONSE_PROMPT
from retrieval import MyTFIDF
from langchain_core.messages.ai import AIMessage


class DanikBotBedrockPipeline:
    def __init__(self):
        # Load environment variables
        env = pydotenv.Environment()
        self._login(env)
        self.model_id = "eu.amazon.nova-micro-v1:0"

        # Initialize Bedrock LLM
        self.llm = ChatBedrock(
            model_id=self.model_id,
            region_name="eu-north-1",
            model_kwargs={
                "maxTokenCount": 1000,
                "temperature": 0.7,
                "topP": 0.9,
            }
        )

        # Retriever (TF-IDF or FAISS)
        self.retriever = MyTFIDF()

        # Safety chain setup
        self.safety_prompt = SAFETY_PROMPT
        self.safety_chain = self.safety_prompt | self.llm.bind(maxTokenCount=20)


    def _login(self, env):
        for i, j in env.items():
            os.environ[i] = j

    @property
    def response_chain(self):
        return RESPONSE_PROMPT | self.llm

    def process_query(self, query: str) -> AIMessage:
        """
        Process the user query through the Bedrock pipeline.
        """

        # Step 1: Retrieve top 5 relevant documents
        top_results = self.retriever.retrieve(query)
        if not top_results:
            return "Извините, по вашему запросу у меня нет данных."

        # Step 2: Concatenate content for context
        context = "\n".join([
            f'{result.page_content}. Метаданные {result.metadata}'
            for result in top_results
        ])

        # Step 3: Generate the answer
        response = self.response_chain.invoke({
            "context": context,
            "query": query
        })

        return response

if __name__=='__main__':
    c = DanikBotBedrockPipeline()
    ans = c.process_query('Бурерлерге қай жерде баруға болады?')
    print(ans)
    print(ans.content)