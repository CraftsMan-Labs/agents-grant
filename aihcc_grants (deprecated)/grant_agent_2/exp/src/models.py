from pydantic import BaseModel
from typing import Optional, List, Dict
import json

class RetrivalQueryModel(BaseModel):
    Question: str
