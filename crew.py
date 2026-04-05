from crewai import Crew, Process
from tasks import create_tasks

def run_crew(question):
    tasks = create_tasks(question)
    crew = Crew(
        agents=[task.agent for task in tasks],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff()
    return result.raw if hasattr(result, 'raw') else str(result)
