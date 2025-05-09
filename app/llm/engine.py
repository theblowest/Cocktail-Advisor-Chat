from typing import List, Dict, Any, Optional
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate

from app.config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS

class LLMEngine:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=MODEL_NAME,
            openai_api_key=OPENAI_API_KEY,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        self.system_prompt = """
        You are the Cocktail Advisor, an expert in cocktails and mixology. 
        Your role is to provide information about cocktails, their ingredients, and preparation methods.
        You can also recommend cocktails based on user preferences and favorite ingredients.
        
        When providing information, always try to be helpful, accurate, and engaging.
        If asked about a specific cocktail, provide its ingredients, preparation method, and any interesting facts about it.
        
        You have access to a database of cocktails and can search for cocktails based on ingredients, categories, or names.
        You also remember the user's preferences and favorite ingredients to provide personalized recommendations.
        
        Always respond in a friendly and conversational manner, as if you're a professional bartender chatting with a customer.
        """
    
    def detect_user_preferences(self, message: str) -> Optional[Dict[str, str]]:
        """
        Detect user preferences from a message
        
        Args:
            message: User message
            
        Returns:
            Dictionary with memory type and content if a preference is detected,
            None otherwise
        """
        # Use LLM to detect if the message contains a preference
        messages = [
            SystemMessage(content="""
            Your task is to analyze the user message and detect if they're sharing a preference about cocktails or ingredients.
            If they are, extract the preference type and content. Respond in JSON format.
            
            Valid preference types:
            - favorite_ingredient: User mentions they like or love a specific ingredient
            - favorite_cocktail: User mentions they like or love a specific cocktail
            - disliked_ingredient: User mentions they dislike a specific ingredient
            
            Example responses:
            {"detected": false}
            {"detected": true, "type": "favorite_ingredient", "content": "rum"}
            """),
            HumanMessage(content=message)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse response
        try:
            import json
            result = json.loads(response.content)
            
            if result.get("detected", False):
                return {
                    "type": result["type"],
                    "content": result["content"]
                }
        except:
            pass
        
        return None
    
    def generate_response(
        self,
        message: str,
        history: List[Dict[str, str]],
        retrieved_context: Optional[str] = None
    ) -> str:
        """
        Generate a response to a user message
        
        Args:
            message: User message
            history: Chat history
            retrieved_context: Context retrieved from vector store
            
        Returns:
            Generated response
        """
        # Convert history to LangChain message format
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Add context if available
        if retrieved_context:
            context_prompt = f"""
            Use the following information to help answer the user's question:
            {retrieved_context}
            
            Only use this information if it's relevant to the question.
            If the information doesn't help, rely on your general knowledge about cocktails.
            """
            messages.append(SystemMessage(content=context_prompt))
        
        # Add history
        for entry in history:
            if entry["role"] == "user":
                messages.append(HumanMessage(content=entry["content"]))
            else:
                messages.append(AIMessage(content=entry["content"]))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        # Generate response
        response = self.llm.invoke(messages)
        
        return response.content