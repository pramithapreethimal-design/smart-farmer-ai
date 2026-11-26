
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    api_key=GROQ_API_KEY
)
