import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

class Config:
    SQL_SERVER_URL = os.getenv("SQL_SERVER_URL")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    
config = Config()