from crewai import Agent

from smart_book_qa.config import configure_llm_api_key
from smart_book_qa.rag_tool import rag_search_tool

configure_llm_api_key()

MODEL_NAME = "gemini/gemini-2.5-flash"

retriever_agent = Agent(
    role="Document Retriever",
    goal="Search the vector store and return the most relevant chunks for the question.",
    backstory=(
        "You are an expert librarian who knows exactly where to find information. "
        "You always search the indexed documents before answering."
    ),
    tools=[rag_search_tool],
    llm=MODEL_NAME,
    verbose=True,
)

writer_agent = Agent(
    role="Answer Writer",
    goal="Write a clear, accurate answer using only the retrieved chunks.",
    backstory=(
        "You explain things simply and only rely on the evidence found in the "
        "uploaded documents."
    ),
    llm=MODEL_NAME,
    verbose=True,
)

checker_agent = Agent(
    role="Quality Checker",
    goal="Verify that the answer is correct, supported, and complete.",
    backstory=(
        "You are a careful fact-checker who compares every claim with the "
        "retrieved document chunks before approving the answer."
    ),
    llm=MODEL_NAME,
    verbose=True,
)
