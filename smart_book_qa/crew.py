from crewai import Crew, Process

from smart_book_qa.config import configure_llm_api_key
from smart_book_qa.tasks import create_tasks


def run_crew(question: str) -> str:
    configure_llm_api_key()
    tasks = create_tasks(question)
    crew = Crew(
        agents=[task.agent for task in tasks],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff()
    return result.raw if hasattr(result, "raw") else str(result)
