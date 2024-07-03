"""
Module to convert data to markdown using LlamaParse.
"""

import os
from llama_parse import LlamaParse
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables from a .env file.
    """
    load_dotenv()

def initialize_parser():
    """
    Initialize and return a LlamaParse parser with the specified configuration.
    
    Returns:
        LlamaParse: An instance of LlamaParse configured with environment variables.
    """
    return LlamaParse(
        api_key=os.getenv("LLAMAINDEX_PARSE_API_KEY"), 
        result_type="markdown", 
        num_workers=4, 
        verbose=True,
        language="en",  
    )

class Parser:
    def __init__(self):
        """
        Initialize the Parser class with LlamaParse configuration.
        """
        load_environment()
        self.parser = initialize_parser()
    
    async def convert_to_md(self, data_path: str):
        """
        Convert data to markdown format using the LlamaParse parser.
        
        Args:
            data_path (str): The path to the data to be converted.
        
        Returns:
            The parsed documents in markdown format.
        """
        return self.parser.parse(data_path)
