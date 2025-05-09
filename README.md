Cocktail Advisor Chat
A Python-based RAG (Retrieval-Augmented Generation) chat application that helps users discover and learn about cocktails. This application integrates an LLM with a vector database to provide intelligent responses about cocktails, store user preferences, and generate personalized recommendations.
Features

Natural Language Chat: Ask questions about cocktails in natural language
Memory Management: System remembers your favorite ingredients and cocktails
Cocktail Recommendations: Get personalized cocktail recommendations based on your preferences
Ingredient-Based Search: Find cocktails containing specific ingredients
Non-Alcoholic Options: Discover non-alcoholic cocktail alternatives
Web-Based Interface: A clean and responsive chat UI

Demo Use Cases

"What are the 5 cocktails containing lemon?"
"What are the 5 non-alcoholic cocktails containing sugar?"
"I love rum and tequila" (stores user preference)
"What are my favourite ingredients?"
"Recommend 5 cocktails that contain my favourite ingredients"
"Recommend a cocktail similar to 'Hot Creamy Bush'"

Tech Stack

Backend: FastAPI
LLM Integration: OpenAI GPT models via LangChain
Vector Database: ChromaDB (FAISS)
Frontend: HTML, CSS, JavaScript
Data Processing: Pandas, KaggleHub

Installation
Prerequisites

Python 3.9+
pip (Python package manager)
OpenAI API key

Setup Instructions

Clone the repository

Create a virtual environment:
bashpython -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

Install the dependencies:
bash pip install -r requirements.txt

Create a .env file in the root directory:
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-3.5-turbo

Run the application:
python main.py

Implementation Details

RAG Architecture
The application uses a Retrieval-Augmented Generation (RAG) architecture to enhance the LLM's responses:

Vector Database: Cocktail data and user preferences are stored in ChromaDB, a vector database with FAISS indexing
Query Processing: When a user asks a question, the system processes it to determine search strategy
Context Retrieval: Relevant cocktail information and user preferences are retrieved from the vector store
Enhanced Generation: The LLM generates responses using both its internal knowledge and the retrieved context

Memory Management
The application detects and stores user preferences:

When a user mentions favorite ingredients or cocktails, the system extracts this information
Preferences are stored in the vector database for future retrieval
Recommendations are personalized based on stored preferences

Search Capabilities
The system can search for cocktails based on various criteria:

Ingredient-based search (e.g., "cocktails with lemon")
Alcoholic/non-alcoholic filtering
Similarity-based recommendations

Limitations and Future Improvements

Ingredient Recognition: The system could benefit from more sophisticated ingredient detection
Multi-Turn Dialog: Enhanced conversation memory for more fluid multi-turn dialog
Image Support: Adding cocktail images would improve the user experience
User Authentication: Adding user accounts to maintain personal preference profiles

Development Process
This project was developed following these steps:

Project Planning: Defined requirements and architecture
Data Processing: Set up cocktail dataset loading and processing
Vector Database: Implemented ChromaDB integration for efficient retrieval
LLM Integration: Connected OpenAI APIs via LangChain
RAG Implementation: Developed the retrieval-augmentation pipeline
Memory Management: Created user preference extraction and storage
API Development: Built FastAPI endpoints for chat functionality
Frontend Development: Created a responsive chat interface
Testing & Refinement: Tested with sample queries and refined the system
