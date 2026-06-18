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

_system_prompt = """You are a document assistant. You can only answer questions based on the documents the user has uploaded.

Always use the retriever_tool to search the documents before answering.
If the retrieved content does not contain enough information to answer the question, say: "I couldn't find that information in the uploaded document."
Never use your general knowledge to answer — only use what is in the documents."""

_agent = create_react_agent(_llm, [retriever_tool, calculator_tool], prompt=_system_prompt)


def run_agent(query: str) -> str:
    result = _agent.invoke({"messages": [("human", query)]})
    return result["messages"][-1].content
