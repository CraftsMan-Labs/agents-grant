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
        load_environment()
        self.parser = initialize_parser()
    
    async def convert_and_save_to_md(self, data_path: str, md_file_path: str):
        """
        Convert data to markdown format and save to specified file path.
        
        Args:
            data_path (str): The path to the data to be converted.
            md_file_path (str): The path where the markdown files will be saved.
        """
        document = self.parser.load_data(data_path)
        for i in range(len(document)):
            file_name = data_path.split("/")[-1].split(".")[0]
            with open(f"{md_file_path}/{file_name}_{i}", "w") as f:
                f.write(document[i].text)
    
    async def convert_to_md(self, data_path: str):
        """
        Convert data to markdown format using the LlamaParse parser.
        
        Args:
            data_path (str): The path to the data to be converted.
        
        Returns:
            The parsed documents in markdown format.
        """
        document = self.parser.load_data(data_path)
        return document
        