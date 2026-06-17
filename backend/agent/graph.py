import os
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from backend.agent.tools import retriever_tool, calculator_tool
from dotenv import load_dotenv

load_dotenv()

_llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
)

_agent = create_react_agent(_llm, [retriever_tool, calculator_tool])


def run_agent(query: str) -> str:
    result = _agent.invoke({"messages": [("human", query)]})
    return result["messages"][-1].content
