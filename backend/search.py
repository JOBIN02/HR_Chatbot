# backend/search.py

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import ollama  # Import the new ollama library

class RAGSystem:
    """
    A class to handle the RAG pipeline using a local LLM with Ollama.
    """
    def __init__(self, data_path="employees.json", model_name='all-MiniLM-L6-v2'):
        """
        Initializes the RAG system.
        """
        print("Initializing RAG System with local LLM...")
        self.data_path = data_path
        self.employees = self._load_data()
        
        # The embedding model remains the same
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
        # We don't need an OpenAI client anymore. Ollama is handled directly.
        
        self.index = self._build_faiss_index()
        print("RAG System initialized successfully.")

    def _load_data(self):
        """Loads employee data from the JSON file."""
        try:
            with open(self.data_path, 'r') as f:
                print(f"Loading data from {self.data_path}...")
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file not found at {self.data_path}")
            return []

    def _prepare_documents(self):
        """Prepares a text document for each employee for embedding."""
        documents = []
        for emp in self.employees:
            doc = (
                f"Name: {emp['name']}. "
                f"Experience: {emp['experience_years']} years. "
                f"Skills: {', '.join(emp['skills'])}. "
                f"Past Projects: {', '.join(emp['past_projects'])}. "
                f"Availability: {emp['availability']}."
            )
            documents.append(doc)
        return documents

    def _build_faiss_index(self):
        """Builds a FAISS index for efficient similarity search."""
        print("Preparing documents for indexing...")
        documents = self._prepare_documents()
        if not documents:
            print("No documents to index.")
            return None
            
        print("Generating embeddings for all documents...")
        embeddings = self.embedding_model.encode(documents, convert_to_tensor=False)
        embeddings = np.array(embeddings).astype('float32')
        
        d = embeddings.shape[1]
        print(f"Building FAISS index with dimension {d}...")
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        print(f"FAISS index built with {index.ntotal} vectors.")
        return index

    def retrieve(self, query, k=3):
        """Retrieves the top-k most relevant employees for a given query."""
        if self.index is None:
            print("FAISS index is not available.")
            return []
            
        print(f"Retrieving top {k} results for query: '{query}'")
        query_embedding = self.embedding_model.encode([query], convert_to_tensor=False).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        retrieved_employees = [self.employees[i] for i in indices[0]]
        print(f"Retrieved {len(retrieved_employees)} employees.")
        return retrieved_employees

    def generate_response(self, query, retrieved_employees):
        """
        Generates a natural language response using a local LLM via Ollama.
        """
        if not retrieved_employees:
            return "I couldn't find any employees that match your query. Could you please try rephrasing it?"

        # The prompt engineering (augmentation) step is the same
        context = "You are an intelligent HR assistant. Your task is to help find the best employees for a project based on the user's query and the provided employee profiles.\n\n"
        context += f"User Query: \"{query}\"\n\n"
        context += "Here are the most relevant employee profiles I found:\n\n"

        for i, emp in enumerate(retrieved_employees, 1):
            context += f"--- Candidate {i} ---\n"
            context += f"Name: {emp['name']}\n"
            context += f"Experience: {emp['experience_years']} years\n"
            context += f"Skills: {', '.join(emp['skills'])}\n"
            context += f"Past Projects: {', '.join(emp['past_projects'])}\n"
            context += f"Availability: {emp['availability']}\n\n"

        context += "Based on this information, please provide a helpful Recommend the best candidates."

        print("Generating response with local LLM (Ollama)...")
        try:
            # This is the new part: calling the Ollama API
            response = ollama.chat(
                model='llama3', # The model you pulled with 'ollama pull'
                messages=[
                    {'role': 'user', 'content': context}
                ],
                options= {
                     "temperature": 0.2  # 👈 add temperature here
                }
                
            )
            return response['message']['content']
        except Exception as e:
            print(f"An error occurred with Ollama: {e}")
            return "Sorry, I'm having trouble connecting to my local AI model right now. Is the Ollama application running?"

    def process_query(self, query):
        """Processes a user query through the full RAG pipeline."""
        print(f"\nProcessing new query: '{query}'")
        retrieved_docs = self.retrieve(query, k=3)
        final_response = self.generate_response(query, retrieved_docs)
        

        print("Response generated.")
        return final_response
