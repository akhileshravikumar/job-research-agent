# Job Research Agent

An AI agent that researches companies using real-time web search.
Built with LangGraph (v1.0), LangChain, and Tavily.

## What it does
Given a company name, the agent autonomously searches the web and returns a structured summary:
- Core product/service
- Location and Dublin presence
- Company size
- Tech stack
- Recent news

## Architecture

User Input
↓
LLM (gpt-4o-mini) — decides what to search
↓
Tavily Web Search Tool — fetches real-time results
↓
LLM — reasons over results, formats output
↓
Structured Company Summary

The agent runs a ReAct loop (Reason → Act → Observe) until it has enough information to answer.

## Tech Stack
- **LangGraph v1.0** — agent orchestration framework
- **OpenAI gpt-4o-mini** — reasoning and generation
- **Tavily Search API** — real-time web search
- **Python 3.11**

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/job-research-agent
cd job-research-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your API keys to a `.env` file:
OPENAI_API_KEY=your-key
TAVILY_API_KEY=your-key

## Usage

```bash
python -m src.agent
```

## Why these tools?
- **LangGraph over plain LangChain:** LangGraph handles stateful loops and complex routing. For a single-turn chain, LangChain is fine. For an agent that needs to decide when to stop searching, you need a graph.
- **Tavily over SerpAPI:** Tavily returns LLM-ready summaries in one API call. SerpAPI returns raw links you'd have to fetch and parse yourself.
- **gpt-4o-mini over gpt-4o:** This task doesn't require frontier reasoning. gpt-4o-mini handles tool calling reliably at 10x lower cost.
