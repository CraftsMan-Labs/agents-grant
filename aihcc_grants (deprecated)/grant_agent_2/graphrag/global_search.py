import os
import pandas as pd
import tiktoken
from dotenv import load_dotenv
from graphrag.query.indexer_adapters import read_indexer_entities, read_indexer_reports
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.global_search.community_context import GlobalCommunityContext
from graphrag.query.structured_search.global_search.search import GlobalSearch


def load_environment_variables():
    """
    Load environment variables from the .env file.

    Returns:
        tuple: A tuple containing the GRAPHRAG API key and the LLM model name.
    """
    load_dotenv()
    return os.environ["GRAPHRAG_API_KEY"], os.environ["GRAPHRAG_LLM_MODEL"]


def initialize_llm(api_key, model):
    """
    Initialize the language model (LLM) using the provided API key and model name.

    Args:
        api_key (str): The API key for accessing the LLM.
        model (str): The name of the LLM model to use.

    Returns:
        ChatOpenAI: An instance of ChatOpenAI configured with the specified parameters.
    """
    return ChatOpenAI(
        api_key=api_key,
        model=model,
        api_type=OpenaiApiType.OpenAI,
        max_retries=20,
    )


def load_data(input_dir, entity_table, community_report_table, entity_embedding_table):
    """
    Load data from parquet files.

    Args:
        input_dir (str): The directory containing the input parquet files.
        entity_table (str): The name of the entity table file.
        community_report_table (str): The name of the community report table file.
        entity_embedding_table (str): The name of the entity embedding table file.

    Returns:
        tuple: A tuple containing DataFrames for entities, reports, and entity embeddings.
    """
    entity_df = pd.read_parquet(f"{input_dir}/{entity_table}.parquet")
    report_df = pd.read_parquet(
        f"{input_dir}/{community_report_table}.parquet")
    entity_embedding_df = pd.read_parquet(
        f"{input_dir}/{entity_embedding_table}.parquet")
    return entity_df, report_df, entity_embedding_df


def initialize_context_builder(reports, entities, token_encoder):
    """
    Initialize the context builder for global community context.

    Args:
        reports (DataFrame): A DataFrame containing the community reports.
        entities (DataFrame): A DataFrame containing the entities.
        token_encoder (object): The token encoder to use.

    Returns:
        GlobalCommunityContext: An instance of GlobalCommunityContext configured with the specified parameters.
    """
    return GlobalCommunityContext(
        community_reports=reports,
        entities=entities,
        token_encoder=token_encoder,
    )


def initialize_search_engine(llm, context_builder, token_encoder):
    """
    Initialize the global search engine.

    Args:
        llm (ChatOpenAI): The language model to use for the search engine.
        context_builder (GlobalCommunityContext): The context builder for the search engine.
        token_encoder (object): The token encoder to use.

    Returns:
        GlobalSearch: An instance of GlobalSearch configured with the specified parameters.
    """
    context_builder_params = {
        "use_community_summary": False,
        "shuffle_data": True,
        "include_community_rank": True,
        "min_community_rank": 0,
        "community_rank_name": "rank",
        "include_community_weight": True,
        "community_weight_name": "occurrence weight",
        "normalize_community_weight": True,
        "max_tokens": 12_000,
        "context_name": "Reports",
    }

    map_llm_params = {
        "max_tokens": 1000,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
    }

    reduce_llm_params = {
        "max_tokens": 2000,
        "temperature": 0.0,
    }

    return GlobalSearch(
        llm=llm,
        context_builder=context_builder,
        token_encoder=token_encoder,
        max_data_tokens=12_000,
        map_llm_params=map_llm_params,
        reduce_llm_params=reduce_llm_params,
        allow_general_knowledge=False,
        json_mode=True,
        context_builder_params=context_builder_params,
        concurrent_coroutines=32,
        response_type="multiple paragraphs",
    )


def main():
    """
    Main function to initialize and configure the global search engine.

    Returns:
        GlobalSearch: An instance of GlobalSearch configured with the specified parameters.
    """
    api_key, llm_model = load_environment_variables()
    llm = initialize_llm(api_key, llm_model)
    token_encoder = tiktoken.get_encoding("cl100k_base")

    input_dir = "/mnt/c/Users/rishu/OneDrive/Desktop/Rishub/AiHCCC/agents-grant/grant_agent_2/graphrag/ragtest/output/20240704-184122/artifacts"
    entity_table = "create_final_nodes"
    community_report_table = "create_final_community_reports"
    entity_embedding_table = "create_final_entities"
    community_level = 2

    entity_df, report_df, entity_embedding_df = load_data(
        input_dir, entity_table, community_report_table, entity_embedding_table)
    reports = read_indexer_reports(report_df, entity_df, community_level)
    entities = read_indexer_entities(
        entity_df, entity_embedding_df, community_level)

    context_builder = initialize_context_builder(
        reports, entities, token_encoder)
    search_engine = initialize_search_engine(
        llm, context_builder, token_encoder)

    return search_engine


search_engine_global = main()


def ask_query_global(query):
    """
    Perform a global search query using the search engine.

    Args:
        query (str): The search query.

    Returns:
        dict: A dictionary containing the search response, LLM calls, prompt tokens, and context data.
    """
    result = search_engine_global.search(query)
    return {
        "response": result.response,
        "llm_calls": result.llm_calls,
        "prompt_tokens": result.prompt_tokens,
        "context_data": result.context_data["reports"]
    }
