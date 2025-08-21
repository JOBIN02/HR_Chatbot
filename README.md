# HR Resource Query Chatbot

This document outlines the project deliverables for the AI-powered HR assistant. The application uses a Retrieval-Augmented Generation (RAG) pipeline and a local LLM via Ollama to help HR teams find the best employees for their needs.

Frontend: Streamlit · Backend: FastAPI

## Project Deliverables

This project fulfills the three core submission requirements: a complete GitHub repository, a working local demo, and comprehensive README.md documentation.

**1. GitHub Repository with Complete Source Code**

The repository is structured with a decoupled frontend and backend for clarity and scalabiliy


# WorkFlow
<img width="1536" height="1024" alt="generated-image (2)" src="https://github.com/user-attachments/assets/6026baa6-6336-4373-aae2-f3948689b15a" />

**2. Working Demo (Local Setup)**
The application is designed to run locally, ensuring data privacy. To run the demo, you will need to start the backend server and the frontend application in two separate terminals. The complete instructions are provided in the Setup and Installation section below.

**3. README.md**
The remainder of this document serves as the project's official README.md, containing the required sections for setup, API documentation, architecture, and the 

**AI development process.**

**Setup and Installation Instructions**

**Prerequisites**

Python 3.8+

Ollama: Install from ollama.com.

**Ollama (Local LLM) Setup**

First, ensure the Ollama application is running. Then, open a terminal and pull the llama3 model.

ollama pull llama3

**Backend Setup**

Navigate to the backend directory, install dependencies, and start the server.

**Go into the backend folder**
cd backend

**Create and activate a virtual environment (recommended)**
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload --port 8000

The backend will be running on http://127.0.0.1:8000.

**Frontend Setup**

Open a new terminal. Navigate to the frontend directory, install dependencies, and run the app.

# Go into the frontend folder
cd frontend

# Activate the same virtual environment
source ../backend/venv/bin/activate # On Windows, use `..\backend\venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

Your browser will open with the chat interface at https://hrchatbot-doyzhqzgzyo6jkgwks5ji4.streamlit.app.

**API Documentation**

GET /employees/search
Performs a simple keyword search over the employee dataset.

Query Parameter: q (string) - The search term.

Example: GET /employees/search?q=python

POST /chat
Processes a natural language query through the full RAG pipeline.

Request Body:

{
  "query": "I need someone with machine learning experience for a healthcare project."
}

Success Response (200 OK):

{
  "response": "Based on your query, Dr. Sarah Chen seems like an excellent fit..."
}

# Architecture Overview
The application follows a decoupled frontend-backend architecture.

<img width="1536" height="1024" alt="generated-image" src="https://github.com/user-attachments/assets/59a77941-d3b2-4c8f-a27e-39df25d07574" />

**User Interaction:** The user types a query into the Streamlit frontend.

**API Call:** The frontend sends a POST request to the /chat endpoint on the FastAPI backend.

**RAG Pipeline (search.py):**

**Retrieve:** The user's query is converted into an embedding vector using sentence-transformers. This vector is used to search the pre-built FAISS index to find the top 3 most semantically similar employee profiles.

**Augment:** The retrieved profiles are combined with the original query to create a detailed context prompt.

**Generate:** This rich prompt is sent to the locally running Ollama instance (llama3 model) to generate a natural language summary.

**Response:** The generated text is sent back through the API to the Streamlit UI to be displayed to the user.

**AI Development Process Section**
This project was built with significant assistance from a generative AI model (Gemini), which acted as a development partner.

**Initial Planning & Scaffolding:** I described the project goal from the assessment. The AI provided a clear end-to-end plan, recommending the FastAPI/Streamlit stack and the RAG architecture. It also generated the initial project structure with backend and frontend folders.

**Code Generation & Adaptation:**

The AI generated the complete, functional code for the RAGSystem class (search.py).

Initially, the code was written for the OpenAI API. When I specified the need to use a local model, the AI seamlessly refactored the code to use the ollama library, demonstrating its ability to adapt to new constraints.

It also generated the complete boilerplate for the FastAPI server (main.py) and the Streamlit UI (app.py).

Debugging & Troubleshooting (Human-AI Collaboration):

Challenge: A significant challenge was a series of FileNotFoundError and ModuleNotFoundError errors caused by an incorrect local file structure, which the AI couldn't "see."

Solution: I provided screenshots of my file structure and terminal errors. The AI analyzed the images, diagnosed the exact problem, and provided the precise commands and steps to fix the structure. This collaborative loop was crucial for overcoming the issue.

Documentation: The AI generated the initial draft of this README.md file, which I then edited and customized with the specific details of my development journey.

Estimated AI-Assisted Code: Approximately 70% of the final code was initially generated by the AI. The remaining 30% involved my direct input: editing, refactoring, debugging based on local errors, and customizing the logic to fit the project's specific needs.
