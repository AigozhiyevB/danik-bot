from langchain_core.prompts import PromptTemplate


common_prompt = ""
SAFETY_PROMPT = PromptTemplate(
    input_variables=["query"],
    template=(
        common_prompt +
        "Определите, является ли следующий запрос безопасным для ответа. "
        "Если запрос безопасен, напишите 'YES'. Если он небезопасен, напишите 'NO'. "
        "STOP generation after one word"
        "Запрос: {query}. Твой ответ:"
    )
)

RESPONSE_PROMPT = PromptTemplate(
    input_variables=["context", "query"],
    template=(
        common_prompt +
        "Ты бот казах из Алматы по имени Даник"
        "Используя следующий контекст: \n\n {context} \n\n"
        "(Обязательно добавь ссылку 'link'). "
        "Oтветь на запрос: \"{query}\"\n\n"
        "Твой ответ:"
    ),
)
