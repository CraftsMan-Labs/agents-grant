from llama_index.core.vector_stores import MetadataFilters, MetadataFilter
import os
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from src.models import RetrivalQueryModel

def initialize_pinecone_index(api_key: str, index_name: str) -> VectorStoreIndex:
    """
    Initialize the Pinecone index and return a VectorStoreIndex.

    Args:
        api_key (str): The API key for Pinecone.
        index_name (str): The name of the Pinecone index.

    Returns:
        VectorStoreIndex: The initialized VectorStoreIndex.
    """
    pc = Pinecone(api_key=api_key)
    pinecone_index = pc.Index(index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    return VectorStoreIndex.from_vector_store(vector_store)

# def retrieve_info(data: RetrivalQueryModel) -> list:
#     """
#     Retrieve country information based on the provided query model.

#     Args:
#         data (RetrivalQueryModel): The query model containing the country and question.

#     Returns:
#         list: The retrieved nodes containing the country information.
#     """
#     index = initialize_pinecone_index(os.getenv("PINECONE_API_KEY",""), os.getenv("PINECONE_INDEX_NAME",""))
    
#     retriever = index.as_retriever()
#     retrieved_nodes = retriever.retrieve(data.Question)
    
#     return retrieved_nodes

from typing import List
from llama_index.embeddings.openai import OpenAIEmbedding

def retrieve_info(data: RetrivalQueryModel, top_n: int = 3) -> List[dict]:
    """
    Retrieve country information based on the provided query model.

    Args:
        data (RetrivalQueryModel): The query model containing the country and question.
        top_n (int): The number of top results to return. Defaults to 3.

    Returns:
        List[dict]: The top N retrieved nodes containing the country information and confidence scores.
    """
    # Initialize Pinecone
    # pinecone.init(api_key=os.getenv("PINECONE_API_KEY", ""), environment=os.getenv("PINECONE_ENVIRONMENT", ""))
    # pinecone_index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME", ""))
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY", ""))
    pinecone_index = pc.Index(os.getenv("PINECONE_INDEX_NAME", ""))

    # Create Pinecone vector store
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    # Create OpenAI embedding model
    embed_model = OpenAIEmbedding()

    # Create vector store index
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    # Create retriever
    retriever = index.as_retriever(similarity_top_k=top_n)

    # Retrieve nodes
    retrieved_nodes = retriever.retrieve(data.Question)

    # Format results with confidence scores
    results = []
    for node in retrieved_nodes:
        results.append({
            "text": node.node.text,
            "confidence": node.score,  # This is the cosine similarity score
            "metadata": node.node.metadata
        })

    # Sort results by confidence score in descending order
    results.sort(key=lambda x: x["confidence"], reverse=True)

    return results