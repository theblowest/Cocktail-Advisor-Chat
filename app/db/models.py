from typing import List, Optional
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    """Model for chat messages"""
    role: str = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    """Model for chat request"""
    message: str = Field(..., description="User message")
    history: List[ChatMessage] = Field(default_factory=list, description="Chat history")

class ChatResponse(BaseModel):
    """Model for chat response"""
    message: str = Field(..., description="Assistant response")
    sources: Optional[List[str]] = Field(default=None, description="Sources used for the response")

class Memory(BaseModel):
    """Model for memory"""
    type: str = Field(..., description="Type of memory")
    content: str = Field(..., description="Content of memory")

class Cocktail(BaseModel):
    """Model for cocktail"""
    name: str
    category: str
    alcoholic: str
    glass: str
    ingredients: List[str]
    measures: Optional[List[str]] = None
    instructions: str