from crewai import Task
from agents import retriever_agent, writer_agent, checker_agent

def create_tasks(question):
    retrieve_task = Task(
        description=f"Search for information about: '{question}'",
        expected_output="Top 3 matching text chunks.",
        agent=retriever_agent
    )

    write_task = Task(
        description=f"Write a clear answer to: '{question}' using only the retrieved chunks.",
        expected_output="A 3-5 sentence answer in simple language.",
        agent=writer_agent
    )

    check_task = Task(
        description="Compare the answer against the source chunks and verify accuracy.",
        expected_output="Return the FULL text of the final written answer, followed by [Status: Verified or Needs Correction].",
        agent=checker_agent
    )

    return [retrieve_task, write_task, check_task]
