"""
Module to convert data to markdown using LlamaParse.
"""

import os
from llama_parse import LlamaParse
from dotenv import load_dotenv

def load_environment():
    load_dotenv()

def initialize_parser():
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
        return self.parser.parse(data_path)
