import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
from typing import List, Dict, Any
import os

from app.config import DATA_DIR, COCKTAILS_DATA

def load_cocktail_data() -> List[Dict[str, Any]]:
    """
    Load cocktail data from Kaggle dataset
    
    Returns:
        List of cocktail dictionaries
    """
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Check if dataset already exists
    if os.path.exists(COCKTAILS_DATA):
        print(f"Loading cocktails from {COCKTAILS_DATA}")
        df = pd.read_csv(COCKTAILS_DATA)
    else:
        print("Downloading cocktails dataset from Kaggle...")
        try:
            # Download dataset from Kaggle
            df = kagglehub.load_dataset(
                KaggleDatasetAdapter.PANDAS,
                "aadyasingh55/cocktails",
                ""  # Empty string to get all files
            )
            
            # Save dataset locally
            df.to_csv(COCKTAILS_DATA, index=False)
            print(f"Saved cocktails dataset to {COCKTAILS_DATA}")
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            # Create an empty DataFrame with the expected columns
            df = pd.DataFrame(columns=[
                "strDrink", "strCategory", "strAlcoholic", "strGlass", "strInstructions"
            ] + [f"strIngredient{i}" for i in range(1, 16)] + [f"strMeasure{i}" for i in range(1, 16)])
    
    # Convert DataFrame to list of dictionaries
    cocktails = df.to_dict(orient="records")
    
    print(f"Loaded {len(cocktails)} cocktails")
    return cocktails

def get_alcoholic_cocktails(cocktails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get alcoholic cocktails
    
    Args:
        cocktails: List of cocktail dictionaries
        
    Returns:
        List of alcoholic cocktail dictionaries
    """
    return [c for c in cocktails if c.get("strAlcoholic", "").lower() == "alcoholic"]

def get_non_alcoholic_cocktails(cocktails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get non-alcoholic cocktails
    
    Args:
        cocktails: List of cocktail dictionaries
        
    Returns:
        List of non-alcoholic cocktail dictionaries
    """
    return [c for c in cocktails if c.get("strAlcoholic", "").lower() == "non alcoholic"]

def get_cocktails_with_ingredient(cocktails: List[Dict[str, Any]], ingredient: str) -> List[Dict[str, Any]]:
    """
    Get cocktails containing a specific ingredient
    
    Args:
        cocktails: List of cocktail dictionaries
        ingredient: Ingredient to search for
        
    Returns:
        List of cocktail dictionaries containing the ingredient
    """
    result = []
    ingredient_lower = ingredient.lower()
    
    for cocktail in cocktails:
        # Check all ingredient fields
        for i in range(1, 16):
            ing_key = f"strIngredient{i}"
            if ing_key in cocktail and cocktail[ing_key] and ingredient_lower in str(cocktail[ing_key]).lower():
                result.append(cocktail)
                break
    
    return result