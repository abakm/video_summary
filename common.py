from pydantic import BaseModel
from pymongo import MongoClient
from langchain_groq import ChatGroq
from typing_extensions import TypedDict


endpoints = {
    "OpenAI": {"url": "https://api.openai.com/v1", "default_model": "gpt-4o", "key_env": "openai"},
    "Groq": {"url": "https://api.groq.com/openai/v1", "default_model": "openai/gpt-oss-120b", "key_env": "groq"},
    "DeepSeek": {"url": "https://api.deepseek.com/v1", "default_model": "deepseek-chat", "key_env": "deepseek"},
    "Perplexity": {"url": "https://api.perplexity.ai", "default_model": "sonar", "key_env": "perplexity"},
    "Google": {"url": "https://generativelanguage.googleapis.com/v1beta/openai", "default_model": "gemini-2.5-flash-lite", "key_env": "generativelanguage"},
    "Hyperbolic": {"url": "https://api.hyperbolic.xyz/v1", "default_model": "meta-llama/Llama-3.3-70B-Instruct", "key_env": "hyperbolic"}
}


class PayloadTemplate(BaseModel):
    source_type: str
    transition: str
    language: str

class State(TypedDict):
    query: str
    email: str
    products: list[dict]
    youtube_link: str

# Database connection
connection = MongoClient("mongodb+srv://shopgenie:shopgenie@cluster0.2zydot4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = connection["Summary"]
video_db = database["video"]

llm = ChatGroq(
    model="llama3-70b-8192",
    api_key="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",
    temperature=0.5,
)
