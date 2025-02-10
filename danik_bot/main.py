import sys
sys.path.append('danik_bot')
from fastapi import FastAPI
from uvicorn import run
from api.routes import router as api_router

app = FastAPI(
    title="Danik Bot",
    description="A LangChain-based chatbot using ISSAI Kazakh LLM for entertainment suggestions in Almaty.",
    version="1.0.0",
)

# Include the API routes
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Danik Bot! Use the /chat endpoint to talk to the bot."}

if __name__=='__main__':
    run(app)