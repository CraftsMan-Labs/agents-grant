import os

import pandas as pd
import tiktoken
from dotenv import load_dotenv

from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey
from graphrag.query.indexer_adapters import (
    read_indexer_entities,
    read_indexer_relationships,
    read_indexer_reports,
    read_indexer_text_units,
)
from graphrag.query.input.loaders.dfs import store_entity_semantic_embeddings
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.embedding import OpenAIEmbedding
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.local_search.mixed_context import LocalSearchMixedContext
from graphrag.query.structured_search.local_search.search import LocalSearch
from graphrag.vector_stores.lancedb import LanceDBVectorStore

# Load environment variables
load_dotenv()

# Constants and configurations
INPUT_DIR = "/mnt/c/Users/rishu/OneDrive/Desktop/Rishub/AiHCCC/agents-grant/grant_agent_2/graphrag/ragtest/output/20240704-184122/artifacts"
LANCEDB_URI = "/mnt/c/Users/rishu/OneDrive/Desktop/Rishub/AiHCCC/agents-grant/grant_agent_2/graphrag/lancedb"
COMMUNITY_REPORT_TABLE = "create_final_community_reports"
ENTITY_TABLE = "create_final_nodes"
ENTITY_EMBEDDING_TABLE = "create_final_entities"
RELATIONSHIP_TABLE = "create_final_relationships"
TEXT_UNIT_TABLE = "create_final_text_units"
COMMUNITY_LEVEL = 2

API_KEY = os.environ["GRAPHRAG_API_KEY"]
LLM_MODEL = os.environ["GRAPHRAG_LLM_MODEL"]
EMBEDDING_MODEL = os.environ["GRAPHRAG_EMBEDDING_MODEL"]

LOCAL_CONTEXT_PARAMS = {
    "text_unit_prop": 0.5,
    "community_prop": 0.1,
    "conversation_history_max_turns": 5,
    "conversation_history_user_turns_only": True,
    "top_k_mapped_entities": 10,
    "top_k_relationships": 10,
    "include_entity_rank": True,
    "include_relationship_weight": True,
    "include_community_rank": False,
    "return_candidate_context": False,
    "embedding_vectorstore_key": EntityVectorStoreKey.ID,
    "max_tokens": 12_000,
}

LLM_PARAMS = {
    "max_tokens": 2_000,
    "temperature": 0.0,
}


def setup_entities():
    """
    Load and read entity data and their embeddings from parquet files.

    Returns:
        DataFrame: A DataFrame containing the entities and their embeddings.
    """
    entity_df = pd.read_parquet(f"{INPUT_DIR}/{ENTITY_TABLE}.parquet")
    entity_embedding_df = pd.read_parquet(
        f"{INPUT_DIR}/{ENTITY_EMBEDDING_TABLE}.parquet")
    return read_indexer_entities(entity_df, entity_embedding_df, COMMUNITY_LEVEL), entity_df


def setup_description_embedding_store(entities):
    """
    Set up the description embedding store and store entity semantic embeddings.

    Args:
        entities (DataFrame): A DataFrame containing the entities and their embeddings.

    Returns:
        LanceDBVectorStore: An instance of LanceDBVectorStore connected to the description embeddings.
    """
    description_embedding_store = LanceDBVectorStore(
        collection_name="entity_description_embeddings")
    description_embedding_store.connect(db_uri=LANCEDB_URI)
    store_entity_semantic_embeddings(
        entities=entities, vectorstore=description_embedding_store)
    return description_embedding_store


def setup_relationships():
    """
    Load and read relationship data from parquet files.

    Returns:
        DataFrame: A DataFrame containing the relationships.
    """
    relationship_df = pd.read_parquet(
        f"{INPUT_DIR}/{RELATIONSHIP_TABLE}.parquet")
    return read_indexer_relationships(relationship_df)


def setup_reports(entity_df):
    """
    Load and read report data from parquet files.

    Args:
        entity_df (DataFrame): A DataFrame containing the entities.

    Returns:
        DataFrame: A DataFrame containing the reports.
    """
    report_df = pd.read_parquet(
        f"{INPUT_DIR}/{COMMUNITY_REPORT_TABLE}.parquet")
    return read_indexer_reports(report_df, entity_df, COMMUNITY_LEVEL)


def setup_text_units():
    """
    Load and read text unit data from parquet files.

    Returns:
        DataFrame: A DataFrame containing the text units.
    """
    text_unit_df = pd.read_parquet(f"{INPUT_DIR}/{TEXT_UNIT_TABLE}.parquet")
    return read_indexer_text_units(text_unit_df)


def setup_llm():
    """
    Set up the language model (LLM) using the OpenAI API.

    Returns:
        ChatOpenAI: An instance of ChatOpenAI configured with the specified parameters.
    """
    return ChatOpenAI(
        api_key=API_KEY,
        model=LLM_MODEL,
        api_type=OpenaiApiType.OpenAI,
        max_retries=20,
    )


def setup_text_embedder():
    """
    Set up the text embedder using the OpenAI API.

    Returns:
        OpenAIEmbedding: An instance of OpenAIEmbedding configured with the specified parameters.
    """
    return OpenAIEmbedding(
        api_key=API_KEY,
        api_base=None,
        api_type=OpenaiApiType.OpenAI,
        model=EMBEDDING_MODEL,
        deployment_name=EMBEDDING_MODEL,
        max_retries=20,
    )


def setup_search_engine():
    """
    Set up the search engine by initializing all necessary components.

    Returns:
        LocalSearch: An instance of LocalSearch configured with the specified parameters.
    """
    entities, entity_df = setup_entities()
    description_embedding_store = setup_description_embedding_store(entities)
    relationships = setup_relationships()
    reports = setup_reports(entity_df)
    text_units = setup_text_units()
    llm = setup_llm()
    token_encoder = tiktoken.get_encoding("cl100k_base")
    text_embedder = setup_text_embedder()

    context_builder_local = LocalSearchMixedContext(
        community_reports=reports,
        text_units=text_units,
        entities=entities,
        relationships=relationships,
        entity_text_embeddings=description_embedding_store,
        embedding_vectorstore_key=EntityVectorStoreKey.ID,
        text_embedder=text_embedder,
        token_encoder=token_encoder,
    )

    return LocalSearch(
        llm=llm,
        context_builder=context_builder_local,
        token_encoder=token_encoder,
        llm_params=LLM_PARAMS,
        context_builder_params=LOCAL_CONTEXT_PARAMS,
        response_type="multiple paragraphs",
    )


search_engine = setup_search_engine()


def ask_query_local(query):
    """
    Perform a local search query using the search engine.

    Args:
        query (str): The search query.

    Returns:
        dict: A dictionary containing the search response, LLM calls, prompt tokens, and context data.
    """
    result = search_engine.search(query)
    return {
        "response": result.response,
        "llm_calls": result.llm_calls,
        "prompt_tokens": result.prompt_tokens,
        "context_data": result.context_data["reports"],
    }
