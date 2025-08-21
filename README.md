**HR Resource Query Chatbot**

An AI-powered HR assistant that searches employee profiles and recommends the best candidates for a query using a Retrieval-Augmented Generation (RAG) pipeline and a local LLM via Ollama.

Frontend: Streamlit · Backend: FastAPI

**Features**

Semantic Search: Understands the meaning behind queries to find the best employees, not just keyword matches.

RAG Pipeline: Utilizes sentence-transformers for embeddings, FAISS for efficient vector retrieval, and a local Large Language Model (Ollama) for generating human-like summaries.

REST API: Provides a clean interface for both simple keyword searches (/employees/search) and advanced AI chat (/chat).

Local First: Runs entirely on your local machine, ensuring data privacy and zero API costs.

Simple UI: A clean, intuitive chat interface built with Streamlit.

Quick Start (Local Setup)
1. Prerequisites
Python 3.8+

Ollama: Install from ollama.com.

2. Setup Ollama (Local LLM)
First, ensure the Ollama application is running. Then, open a terminal and pull the llama3 model.

ollama pull llama3

3. Backend Setup
Navigate to the backend directory and install its dependencies.

# Go into the backend folder
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload --port 8000

The backend is now running on http://127.0.0.1:8000.

4. Frontend Setup
Open a new terminal. Navigate to the frontend directory.

# Go into the frontend folder
cd frontend

# Activate the same virtual environment
source ../backend/venv/bin/activate # On Windows, use `..\backend\venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py


**API Documentation**

The backend provides the following endpoints. You can also view interactive documentation via Swagger UI at http://127.0.0.1:8000/docs.

GET /employees/search
Performs a simple keyword search over the employee dataset.

Query Parameter: q (string) - The search term.

Example: GET /employees/search?q=python

Success Response (200 OK):

[
  {
    "id": 1,
    "name": "Alice Johnson",
    "skills": ["Python", "React", "AWS", "Machine Learning", "TensorFlow"],
    "experience_years": 5,
    "past_projects": ["E-commerce Platform Recommendation Engine", "Healthcare Predictive Analytics Dashboard"],
    "availability": "available"
  }
]

POST /chat
Processes a natural language query through the full RAG pipeline.

Request Body:

{
  "query": "I need someone with machine learning experience for a healthcare project."
}

Success Response (200 OK):

{
  "response": "Based on your query, Dr. Sarah Chen seems like an excellent fit. With 6 years of experience in Machine Learning, PyTorch, and specific work on a 'Medical Diagnosis Platform' and 'Patient Risk Prediction System', her background aligns perfectly with a healthcare project. She is also currently available."
}


The application follows a decoupled frontend-backend architecture.

User Interaction: The user types a query into the Streamlit frontend.

API Call: The frontend sends a POST request to the /chat endpoint on the FastAPI backend.

RAG Pipeline (search.py):

Retrieve: The user's query is converted into an embedding vector using sentence-transformers. This vector is used to search the pre-built FAISS index, which finds the top 3 most semantically similar employee profiles.

Augment: The retrieved employee profiles are combined with the original query to create a detailed context prompt.

Generate: This rich prompt is sent to the locally running Ollama instance (llama3 model), which generates a coherent, natural language summary and recommendation.

Response: The generated text is sent back to the FastAPI server, which then relays it to the Streamlit UI to be displayed to the user.

**Technical Decisions**

The primary technical decision was to use a local-first approach with Ollama instead of a cloud-based API like OpenAI. This choice was driven by several key factors:

Privacy & Security: Employee data is sensitive. By using Ollama, the entire RAG process runs locally. No data ever leaves the machine, which is a critical requirement for handling internal HR information.

Cost: Cloud-based LLM APIs have usage-based pricing. For an internal tool, this can lead to unpredictable costs. A local model has a one-time setup cost (hardware) but is free to run, making it highly cost-effective for frequent use.

Control & Customization: Running a model locally provides full control over the model version and configuration. It avoids reliance on a third-party service's availability and potential API changes.

Trade-offs: The main trade-off is performance and setup complexity. A powerful local machine is needed to run larger models efficiently, and the initial setup of Ollama and the model is more involved than simply using a cloud API key. However, for this use case, the benefits of privacy and cost far outweigh these drawbacks.

**AI Development Process**

This project was built with significant assistance from a generative AI model (Gemini), which acted as a development partner throughout the process.

Initial Planning & Scaffolding: I described the project goal from the assessment. The AI provided a clear end-to-end plan, recommending the FastAPI/Streamlit stack and the RAG architecture. It also generated the initial project structure with backend and frontend folders.

Code Generation & Adaptation:

The AI generated the complete, functional code for the RAGSystem class (search.py), including the logic for creating embeddings, building the FAISS index, and interacting with an LLM.

Initially, the code was written for the OpenAI API. When I specified the need to use a local model, the AI seamlessly refactored the code to use the ollama library, demonstrating its ability to adapt to new constraints.

It also generated the complete boilerplate for the FastAPI server (main.py) and the Streamlit UI (app.py).

Debugging & Troubleshooting (Human-AI Collaboration):

Challenge Where AI Couldn't Help Directly: A significant challenge was a series of FileNotFoundError and ModuleNotFoundError errors. The AI's initial advice was generic. The problem was my local file structure, which the AI couldn't "see."

How We Solved It: I provided screenshots of my file structure and terminal errors. The AI was then able to analyze the images, diagnose the exact problem (files not being in the correct backend/frontend folders), and provide the precise commands and steps to fix the structure. This collaborative loop was crucial for overcoming the issue.

Documentation: The AI generated the initial draft of this README.md file, which I then edited and customized with the specific details of my development journey.

Estimated AI-Assisted Code: Approximately 70% of the final code was initially generated by the AI. The remaining 30% involved my direct input: editing, refactoring, debugging based on local errors, and customizing the logic to fit the project's specific needs.

**Future Improvements**

With more time, the following features could be added:

Database Integration: Replace the employees.json file with a robust database (like PostgreSQL or SQLite) to allow for easier management of employee data.

Follow-up Questions: Implement conversation memory so the user can ask follow-up questions (e.g., "Of those, who is available?").

UI Enhancements: Add filters and sorting options to the Streamlit UI to allow HR to manually browse and filter the full employee list.

Authentication: Add a login layer to secure the application.

Your browser should open with the chat interface at http://localhost:8501.

