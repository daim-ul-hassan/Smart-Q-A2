import os
from crewai import Agent
from rag_tool import rag_search_tool
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "")

retriever_agent = Agent(
    role='Document Retriever',
    goal='Search the vector store and return the most relevant chunks for the question',
    backstory='You are an expert librarian who knows exactly where to find information.',
    tools=[rag_search_tool],
    llm='gemini/gemini-2.0-flash',
    verbose=True
)

writer_agent = Agent(
    role='Answer Writer',
    goal='Read the retrieved chunks and write a clear, accurate answer in simple language',
    backstory='You are a friendly teacher who explains things clearly using only provided facts.',
    llm='gemini/gemini-2.0-flash',
    verbose=True
)

checker_agent = Agent(
    role='Quality Checker',
    goal='Check the answer against the source chunks and confirm it is correct',
    backstory='You are a careful fact-checker who ensures every fact is accurate.',
    llm='gemini/gemini-2.0-flash',
    verbose=True
)
