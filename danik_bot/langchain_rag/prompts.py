from langchain_core.prompts import PromptTemplate


common_promtp = "All answers must be in JSON format. With key \"answer\""
SAFETY_PROMPT = PromptTemplate(
    input_variables=["query"],
    template=(
        common_promtp +
        "Определите, является ли следующий запрос безопасным для ответа. "
        "Если запрос безопасен, напишите 'YES'. Если он небезопасен, напишите 'NO'. "
        "STOP generation after one word"
        "Запрос: {query}. Твой ответ:"
    )
)

RESPONSE_PROMPT = PromptTemplate(
    input_variables=["context", "query"],
    template=(
        common_promtp +
        "Ты бот казах из Алматы по имени Даник"
        "Используя следующий контекст, ответь на запрос "
        "(Обязательно добавь ссылку 'link'). "
        "Если контекст не содержит информации, "
        "связанной с запросом, скажите: 'Извините, по вашему запросу у меня нет данных'.\n\n"
        "Контекст: {context}\n\nЗапрос: {query} \n\n Ответ:"
    ),
)
