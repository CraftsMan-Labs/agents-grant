from llama_parse import LlamaParse
from dotenv import load_dotenv
import os

load_dotenv()

class Parser:
    def __init__(self):
        self.parser = LlamaParse(
            api_key=os.getenv("LLAMAINDEX_PARSE_API_KEY"), 
            result_type="markdown", 
            num_workers=4, 
            verbose=True,
            language="en",  
        )
