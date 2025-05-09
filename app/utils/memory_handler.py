from typing import List, Dict, Any, Optional
import re

class MemoryHandler:
    @staticmethod
    def extract_favorite_ingredients(text: str) -> List[str]:
        """
        Extract favorite ingredients from text
        
        Args:
            text: Text to extract from
            
        Returns:
            List of extracted ingredients
        """
        # Look for patterns like "I like X" or "My favorite ingredient is X"
        patterns = [
            r"(?:I|i) (?:like|love|enjoy|prefer) (\w+)",
            r"(?:my|My) favorite (?:ingredient|liquor|spirit|drink) is (\w+)",
            r"(\w+) is my favorite (?:ingredient|liquor|spirit|drink)"
        ]
        
        ingredients = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            ingredients.extend(matches)
        
        return ingredients
    
    @staticmethod
    def extract_favorite_cocktails(text: str) -> List[str]:
        """
        Extract favorite cocktails from text
        
        Args:
            text: Text to extract from
            
        Returns:
            List of extracted cocktails
        """
        # Look for patterns like "I like X cocktail" or "My favorite cocktail is X"
        patterns = [
            r"(?:I|i) (?:like|love|enjoy|prefer) (?:the )?(\w+(?:\s\w+)*) (?:cocktail|drink)",
            r"(?:my|My) favorite (?:cocktail|drink) is (?:the )?(\w+(?:\s\w+)*)",
            r"(\w+(?:\s\w+)*) is my favorite (?:cocktail|drink)"
        ]
        
        cocktails = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            cocktails.extend(matches)
        
        return cocktails