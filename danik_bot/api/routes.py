from fastapi import APIRouter, HTTPException
from danik_bot.langchain.chat import ChatBot

router = APIRouter()

# Initialize the chatbot
chatbot = ChatBot()

@router.post("/chat")
async def chat(user_input: str):
    """
    Chat endpoint for the chatbot.

    Args:
        user_input (str): The user's input message.

    Returns:
        dict: The chatbot's response.
    """
    if not user_input:
        raise HTTPException(status_code=400, detail="Input cannot be empty.")
    response = chatbot.generate_response(user_input)
    return {"user_input": user_input, "response": response}
