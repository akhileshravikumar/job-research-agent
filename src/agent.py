# src/agent.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from src.tools import get_search_tool

# Load API keys from .env file
load_dotenv()


def build_agent():
    """
    Builds and returns a ReAct agent.
    
    DECISION: Why create_react_agent (prebuilt) vs building manually?
    
    LangGraph has two ways to build agents:
    1. create_react_agent — a prebuilt function that wires everything for you
    2. StateGraph — build the graph manually, node by node
    
    We're using the prebuilt version this week because:
    - You can get a working agent in 10 lines
    - It implements the full ReAct loop correctly
    - Week 2 you'll graduate to building the graph manually, which is when
      you need finer control (multiple agents, custom routing logic)
    
    DECISION: Why gpt-4o-mini?
    - cheapest capable model from OpenAI (~$0.15/1M input tokens)
    - fully supports tool calling (required for agents)
    - gpt-4o is ~10x the cost for this task — overkill at this stage
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0  # temperature=0 means deterministic output
                       # we want consistent, factual research, not creative text
    )

    tools = [get_search_tool()]

    """
    DECISION: Why MemorySaver?
    
    Without a checkpointer, the agent forgets the entire conversation
    after each .invoke() call. MemorySaver stores state in Python's
    in-process memory — simple, no database needed, perfect for development.
    
    In production you'd swap this for a PostgresSaver or RedisSaver
    so state survives server restarts.
    """
    memory = MemorySaver()

    system_prompt = """You are a company research assistant. 
    When given a company name, search for information about them and return a structured summary covering:
    1. What the company does (core product/service)
    2. Where they are headquartered and if they have Dublin offices
    3. Their approximate size (employees, funding stage, or revenue if public)
    4. Their main technology stack or domain (if available)
    5. One recent notable news item
    6. Having vacancies for software engineers, developers, AI/ML Engineers, Data Analysts, Full-Stack Developers (if available)
    Be concise and factual. Only include information you found via search."""

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt = system_prompt,
        checkpointer=memory
    )

    return agent


def research_company(company_name: str) -> str:
    """
    Takes a company name, runs the agent, returns a structured summary.
    
    The thread_id in config is how LangGraph tracks conversation history.
    Each unique thread_id is a separate conversation with its own memory.
    Using the company name as thread_id means if you research the same
    company twice in one session, it remembers the previous search.
    """
    agent = build_agent()

    config = {"configurable": {"thread_id": company_name}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Research this company: {company_name}"}]},
        config=config
    )

    # result["messages"] is a list of all messages in the conversation
    # The last message is always the agent's final response
    final_message = result["messages"][-1]
    return final_message.content


if __name__ == "__main__":
    company = input("Enter a company name to research: ")
    print(f"\nResearching {company}...\n")
    summary = research_company(company)
    print(summary)