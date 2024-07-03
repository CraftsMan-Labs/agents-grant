"""
Module to convert data to markdown using LlamaParse.
"""

from llama_parse import LlamaParse
from dotenv import load_dotenv
import os

load_dotenv()

class Parser:
    def __init__(self):
        """
        Initialize the Parser class with LlamaParse configuration.
        """
        self.parser = LlamaParse(
            api_key=os.getenv("LLAMAINDEX_PARSE_API_KEY"), 
            result_type="markdown", 
            num_workers=4, 
            verbose=True,
            language="en",  
        )
    
    async def convert_to_md(self, data_path:str):
        documents = self.parser.parse(data_path)
        return documents
