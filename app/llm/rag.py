from typing import List, Dict, Any, Optional, Tuple
from langchain.schema import Document

from app.db.vector_store import VectorStore
from app.llm.engine import LLMEngine

class CocktailRAG:
    def __init__(self, vector_store: VectorStore, llm_engine: LLMEngine):
        self.vector_store = vector_store
        self.llm_engine = llm_engine
    
    def process_query(
        self,
        query: str,
        history: List[Dict[str, str]]
    ) -> Tuple[str, List[str]]:
        """
        Process a user query using RAG
        
        Args:
            query: User query
            history: Chat history
            
        Returns:
            Tuple of (response, sources)
        """
        # Detect user preferences
        preference = self.llm_engine.detect_user_preferences(query)
        if preference:
            # Store user preference
            self.vector_store.add_user_memory(
                memory_text=f"My {preference['type']} is {preference['content']}",
                memory_type=preference["type"]
            )
        
        # Analyze query to determine search strategy
        search_strategy = self._determine_search_strategy(query)
        
        # Retrieve relevant information
        retrieved_docs = []
        sources = []
        
        if search_strategy.get("search_cocktails", False):
            cocktail_docs = self.vector_store.search_cocktails(query)
            retrieved_docs.extend(cocktail_docs)
            sources.extend([doc.metadata.get("name", "Unknown") for doc in cocktail_docs])
        
        if search_strategy.get("search_user_memories", False):
            memory_docs = self.vector_store.get_user_memories(query)
            retrieved_docs.extend(memory_docs)
        
        if search_strategy.get("get_favorites", False):
            favorite_ingredients = self.vector_store.get_favorite_ingredients()
            if favorite_ingredients:
                favorites_text = f"User's favorite ingredients: {', '.join(favorite_ingredients)}"
                retrieved_docs.append(Document(page_content=favorites_text))
        
        if search_strategy.get("recommend_similar", False):
            # Extract cocktail name from query
            cocktail_name = self._extract_cocktail_name(query)
            if cocktail_name:
                similar_docs = self.vector_store.search_cocktails(f"Cocktail similar to {cocktail_name}")
                retrieved_docs.extend(similar_docs)
                sources.extend([doc.metadata.get("name", "Unknown") for doc in similar_docs])
        
        # Combine retrieved documents into context
        context = self._combine_documents(retrieved_docs)
        
        # Generate response using LLM
        response = self.llm_engine.generate_response(query, history, context)
        
        return response, list(set(sources))
    
    def _determine_search_strategy(self, query: str) -> Dict[str, bool]:
        """
        Determine search strategy based on the query
        
        Args:
            query: User query
            
        Returns:
            Dictionary of search strategies to use
        """
        query_lower = query.lower()
        strategy = {
            "search_cocktails": False,
            "search_user_memories": False,
            "get_favorites": False,
            "recommend_similar": False
        }
        
        # Check if query is about cocktails
        if any(word in query_lower for word in ["cocktail", "drink", "recipe", "ingredients", "mix", "contain"]):
            strategy["search_cocktails"] = True
        
        # Check if query is about user preferences
        if any(word in query_lower for word in ["favorite", "prefer", "like", "love"]):
            strategy["search_user_memories"] = True
        
        # Check if query is asking for recommendations
        if any(word in query_lower for word in ["recommend", "suggestion", "what should"]):
            strategy["search_cocktails"] = True
            strategy["search_user_memories"] = True
            strategy["get_favorites"] = True
        
        # Check if query is asking for similar cocktails
        if "similar" in query_lower:
            strategy["recommend_similar"] = True
        
        return strategy
    
    def _extract_cocktail_name(self, query: str) -> Optional[str]:
        """
        Extract cocktail name from query
        
        Args:
            query: User query
            
        Returns:
            Cocktail name if found, None otherwise
        """
        query_lower = query.lower()
        
        # Look for patterns like "similar to X" or "like X"
        patterns = ["similar to", "like"]
        
        for pattern in patterns:
            if pattern in query_lower:
                parts = query_lower.split(pattern, 1)
                if len(parts) > 1:
                    # Extract the cocktail name
                    cocktail_name = parts[1].strip()
                    # Remove any trailing punctuation or text
                    for punctuation in [".", ",", "?", "!", ";"]:
                        if punctuation in cocktail_name:
                            cocktail_name = cocktail_name.split(punctuation, 1)[0]
                    
                    # Remove quotes if present
                    cocktail_name = cocktail_name.strip('"\'')
                    
                    return cocktail_name
        
        return None
    
    def _combine_documents(self, documents: List[Document]) -> str:
        """
        Combine documents into a single context string
        
        Args:
            documents: List of documents
            
        Returns:
            Combined context string
        """
        if not documents:
            return ""
        
        context_parts = []
        
        for doc in documents:
            context_parts.append(doc.page_content)
        
        return "\n\n".join(context_parts)