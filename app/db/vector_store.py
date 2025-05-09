import os
import numpy as np
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_chroma import Chroma
from langchain.schema import Document

from app.config import VECTOR_DB_PATH, OPENAI_API_KEY

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        
        # Initialize vector stores for different collections
        self.cocktail_db = self._init_vector_store("cocktails")
        self.user_memory_db = self._init_vector_store("user_memories")
    
    def _init_vector_store(self, collection_name: str) -> Chroma:
        """Initialize a vector store with the given collection name"""
        persist_directory = os.path.join(VECTOR_DB_PATH, collection_name)
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        return Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
    
    def add_cocktails(self, cocktails: List[Dict[str, Any]]) -> None:
        """
        Add cocktails to the vector store
        
        Args:
            cocktails: List of cocktail dictionaries
        """
        documents = []
        
        for i, cocktail in enumerate(cocktails):
            # Create a formatted string representation of the cocktail
            cocktail_text = f"Name: {cocktail['name']}\n"
            cocktail_text += f"Category: {cocktail['category']}\n"
            cocktail_text += f"Alcoholic: {cocktail['alcoholic']}\n"
            cocktail_text += f"Glass: {cocktail['glassType']}\n"
            cocktail_text += f"Ingredients: {cocktail.get('ingredients', '')}\n"
            cocktail_text += f"Ingredient Measures: {cocktail.get('ingredientMeasures', '')}\n"
            cocktail_text += f"Instructions: {cocktail['instructions']}\n"
            
            # Create document
            doc = Document(
                page_content=cocktail_text,
                metadata={
                    "id": str(i),
                    "name": cocktail['name'],
                    "category": cocktail['category'],
                    "alcoholic": cocktail['alcoholic'],
                    "glass": cocktail['glassType'],
                    "ingredients": cocktail.get('ingredients', ''),
                    "measures": cocktail.get('ingredientMeasures', '')
                }
            )
            
            documents.append(doc)
        
        # Add documents to vector store
        self.cocktail_db.add_documents(documents)
        print(f"Added {len(documents)} cocktails to vector store")
    
    def search_cocktails(self, query: str, k: int = 5) -> List[Document]:
        """
        Search for cocktails similar to the query
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar cocktails
        """
        return self.cocktail_db.similarity_search(query, k=k)
    
    def add_user_memory(self, memory_text: str, memory_type: str) -> None:
        """
        Add user memory to the vector store
        
        Args:
            memory_text: Memory text
            memory_type: Type of memory (e.g., "favorite_ingredient", "favorite_cocktail")
        """
        document = Document(
            page_content=memory_text,
            metadata={"type": memory_type}
        )
        
        self.user_memory_db.add_documents([document])
        print(f"Added user memory of type {memory_type}: {memory_text}")
    
    def get_user_memories(self, query: str, k: int = 5) -> List[Document]:
        """
        Get user memories similar to the query
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar memories
        """
        return self.user_memory_db.similarity_search(query, k=k)
    
    def get_favorite_ingredients(self) -> List[str]:
        """
        Get user's favorite ingredients
        
        Returns:
            List of favorite ingredients
        """
        memories = self.user_memory_db.similarity_search("favorite ingredients", k=10)
        ingredients = []
        
        for memory in memories:
            if memory.metadata.get("type") == "favorite_ingredient":
                # Extract ingredient name from memory text
                content = memory.page_content.lower()
                if "favorite" in content and "ingredient" in content:
                    # Try to extract the ingredient from the text
                    parts = content.split("is ")
                    if len(parts) > 1:
                        ingredients.append(parts[1].strip())
        
        return ingredients
