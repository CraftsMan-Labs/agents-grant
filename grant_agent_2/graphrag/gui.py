import time
import os
from typing import List, Optional
import json
import requests
import gradio as gr
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import (PromptTemplate, MessagesPlaceholder,
                                    HumanMessagePromptTemplate, SystemMessagePromptTemplate,
                                    ChatPromptTemplate)
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.tools import tool

# Load environment variables
load_dotenv()

# Database setup
# engine = create_engine('sqlite:///grants.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# Global variable to collect data
collected_data = []


class GrantDetails(BaseModel):
    grant_amount: Optional[str] = Field(
        description="Amount of funding available")
    conditions: Optional[List[str]] = Field(
        description="Conditions and requirements for the grant")
    eligibility_criteria: Optional[List[str]] = Field(
        description="Eligibility criteria for the grant")
    unusual_conditions: Optional[List[str]] = Field(
        description="Any unusual conditions or nuances to consider")
    grant_category: Optional[str] = Field(
        description="Category of the grant (e.g., Business, Non-Profit, Educational, Environmental, Health, Agriculture)")
    additional_info: Optional[str] = Field(
        description="Any additional information about the grant")
    project_name: Optional[str] = Field(description="Name of the project")
    project_description: Optional[str] = Field(
        description="Description of the project")
    project_usecase: Optional[str] = Field(
        description="Usecase of the project")
    project_outcomes: Optional[str] = Field(
        description="Outcomes of the project")
    project_execution_plan: Optional[str] = Field(
        description="Execution plan of the project")
    
class GrantWriteModel(BaseModel):
    grant_name: str
    grant_amount: str
    conditions: List[str]
    eligibility_criteria: List[str]
    grant_category: str
    sponsor: str
    additional_info: str
    project_name: Optional[str] = Field(description="Name of the project")
    project_description: Optional[str] = Field(
        description="Description of the project")
    project_usecase: Optional[str] = Field(
        description="Usecase of the project")
    project_outcomes: Optional[str] = Field(
        description="Outcomes of the project")
    project_execution_plan: Optional[str] = Field(
        description="Execution plan of the project")


@tool
def update_grant_acquisition_requirements(talent_acquisition_requirements: GrantDetails, search_type="local") -> str:
    """
    Search for suitable grants based on the requirements provided.

    Args:
        talent_acquisition_requirements (GrantDetails): The requirements for the grant.
        search_type (str): The type of search to perform, either "global" or "local".

    Returns:
        str: The search results.
    """
    """When a person searching for grants you call this function to search for suitable grants based on the requirements provided."""
    print("--------Function update_talent_acquisition_requirements called--------")
    print("Requirements: ", talent_acquisition_requirements)
    print("--------Function update_talent_acquisition_requirements ended--------")
    params = talent_acquisition_requirements.dict()
    params = [f"{key}={value}" for key, value in params.items() if value]
    query_search = " \n".join(params)
    query_search = "Search for grants based on the following requirements: " + query_search
    query_search = str(query_search)
    # utf-8 encoding
    query_search = query_search.encode('utf-8').decode('utf-8')
    print("Query Search: ", query_search)
    time.sleep(1)
    if search_type == "local":
        # search_results = ask_query_local(params)
        # send a post request to http://localhost:8000/local_search
        url = "http://localhost:8000/local_search"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "query": query_search
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        search_results = response.json()

    else:
        # search_results = ask_query_global(params)
        # send a post request to http://localhost:8000/global_search
        url = "http://localhost:8000/global_search"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "query": query_search
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        search_results = response.json()
    # convert the search results to a string
    print("Search Results: ", search_results)
    search_results = search_results['response']
    return search_results

@tool
def write_sample_grant_document(data: GrantWriteModel) -> str:
    """
    Generate a sample grant document based on the grant details provided.
    """
    llm = ChatOpenAI(
            model='gpt-4o', temperature=0.8, api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"""
    ==========================Grant Details==========================
    Grant Name: {data.grant_name}
    Grant Amount: {data.grant_amount}
    Conditions: {', '.join(data.conditions)}
    Eligibility Criteria: {', '.join(data.eligibility_criteria)}
    Grant Category: {data.grant_category}
    Sponsor: {data.sponsor}
    Additional Info: {data.additional_info}
    Project Name: {data.project_name}
    Project Description: {data.project_description}
    Project Usecase: {data.project_usecase}
    Project Outcomes: {data.project_outcomes}
    Project Execution Plan: {data.project_execution_plan}
    ==============================================================
    INSTRUCTIONS:
    - Update the grant details as needed.

    Write a sample grant document based on the grant details provided above.

    """    

class GrantAcquisitionBot:
    def __init__(self):
        """
        Initialize the GrantAcquisitionBot with necessary configurations.
        """
        self.chat_history = []
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.model_name = 'gpt-4o'
        self.temperature = 0.9
        self.llm = ChatOpenAI(
            model=self.model_name, temperature=self.temperature, api_key=self.openai_key)
        self.system_prompt = self._get_system_prompt()
        self.chat_history.append(SystemMessage(content=self.system_prompt))
        self.tools = [update_grant_acquisition_requirements]
        self.prompt = self._get_prompt_template()
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=agent, tools=self.tools, verbose=True)

    def _get_system_prompt(self):
        """
        Get the system prompt for the chatbot.

        Returns:
            str: The system prompt.
        """
        return """
==========================GREETING==========================
Hi There! I am your grant acquisition specialist. How can I help you today?
=============================================================

===========================INSTRUCTIONS===========================        
Your role is to act as a grant acquisition specialist for a grant acquisition company. Embody the following traits throughout the conversation:
- Friendly, polite, personable, and patient
- The user can change any information they need.
==================================================================

==========================IMPORTANT==========================
Ask questions one at a time and avoid getting sidetracked into off-topic conversations. Keep it simple and short.
=============================================================

========================SAMPLE QUESTIONS========================
What is the name of the grant? (e.g., Industrial Research Assistance Program)
What is the URL of the grant? (e.g., https://nrc.canada.ca/en/support-technology-innovation/industrial-research-assistance-program)
What is the amount of funding available?
What are the conditions and requirements for the grant?
What is the submission timeline for the grant?
What are the eligibility criteria for the grant?
Can you describe the application process?
Are there any unusual conditions or nuances to consider?
What is the category of the grant? (e.g., Business, Non-Profit, Educational, Environmental, Health, Agriculture)
Who is the sponsor or provider of the grant?
Any additional information about the grant?
==================================================================

==========================REQUIREMENTS==========================
Required fields:
- grant_amount
- conditions
- eligibility_criteria
- unusual_conditions
- grant_category
- additional_info
- grants project name
- project_description
- project_usecase
- project_outcomes
- project_execution_plan
============================IMPORTANT==========================
Ask questions one at a time and avoid getting sidetracked into off-topic conversations. Keep it simple and short. Call update_grant_details once all the requirements are gathered from the user.
=============================================================

==========================After recommending a grant==========================
generate a draft docuement on the grant you think is more suitable
=============================================================
"""

    def _get_prompt_template(self):
        """
        Get the prompt template for the chatbot.

        Returns:
            ChatPromptTemplate: The prompt template.
        """
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(prompt=PromptTemplate(
                input_variables=[], template=self.system_prompt)),
            MessagesPlaceholder(variable_name='chat_history', optional=True),
            HumanMessagePromptTemplate(prompt=PromptTemplate(
                input_variables=['input'], template='{input}')),
            MessagesPlaceholder(variable_name='agent_scratchpad')
        ])

    def chat(self, user_input):
        """
        Process user input and generate a response using the chatbot.

        Args:
            user_input (str): The input from the user.

        Returns:
            str: The response from the chatbot.
        """
        response = self.agent_executor.invoke(
            {"input": user_input, "chat_history": self.chat_history})
        return response['output']


bot = GrantAcquisitionBot()


def chat(message, chat_history):
    """
    Handle the chat interaction with the user.

    Args:
        message (str): The message from the user.
        chat_history (list): The chat history.

    Returns:
        str: The response from the chatbot.
    """
    if not chat_history:
        intro_message = "Hi There! I am your Grant acquisition specialist. How can I help you today?"
        bot.chat_history.append(AIMessage(content=intro_message))
    ai_response = bot.chat(message)
    print("AI: ", ai_response)
    bot.chat_history.append(HumanMessage(content=message))
    bot.chat_history.append(AIMessage(content=ai_response))
    return ai_response


def clear_chat_history():
    """
    Clear the chat history and collected data.
    """
    global collected_data
    collected_data = []
    bot.chat_history = []


def display_data():
    """
    Display the collected data.

    Returns:
        dict: The collected data as a dictionary.
    """
    data_dict = {data[0]: data[1] for data in collected_data}
    print("Data Dict: ", data_dict)
    return data_dict


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=3):
            chat_interface = gr.ChatInterface(
                fn=chat,
                title="Grant Acquisition Specialist Chatbot"
            )
        with gr.Column(scale=1):
            button1 = gr.Button("Clear Chat History")
            button1.click(fn=clear_chat_history)

            data_display = gr.JSON(value=display_data(), label="Sidebar Data")
            button2 = gr.Button("Display Data")
            button2.click(fn=display_data, outputs=data_display)

demo.launch()
