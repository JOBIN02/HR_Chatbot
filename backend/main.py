# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from search import RAGSystem   # import your RAG system
import json

app = FastAPI()

# Initialize RAG system once at startup
rag = RAGSystem(data_path="employees.json")

class ChatQuery(BaseModel):
    query: str

@app.get("/employees/search")
def search_employees(q: str = ""):
    if not q:
        return rag.employees
    results = [
        emp for emp in rag.employees
        if q.lower() in str(emp).lower()
    ]
    return results

@app.post("/chat")
def chat_handler(chat_query: ChatQuery):
    response_text = rag.process_query(chat_query.query)
    return {"response": response_text}
