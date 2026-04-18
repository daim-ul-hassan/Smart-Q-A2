from crewai import Task

from smart_book_qa.agents import checker_agent, retriever_agent, writer_agent


def create_tasks(question: str) -> list[Task]:
    retrieve_task = Task(
        description=(
            f"Search the document database for information about: '{question}'.\n"
            "Use the RAG Search Tool to retrieve the 3 most relevant chunks.\n"
            "Return the chunks exactly as found."
        ),
        expected_output="The top 3 matching text chunks from the indexed documents.",
        agent=retriever_agent,
    )

    write_task = Task(
        description=(
            f"Using only the retrieved chunks, answer this question: '{question}'.\n"
            "Write 3-5 clear sentences and do not introduce outside knowledge."
        ),
        expected_output="A concise answer grounded only in the retrieved chunks.",
        agent=writer_agent,
    )

    check_task = Task(
        description=(
            "Compare the answer against the source chunks and verify each claim.\n"
            "Return only the final verified answer in a clean form.\n"
            "Do not include verdict labels, chunk listings, source breakdowns, or extra formatting."
        ),
        expected_output="The final verified answer only.",
        agent=checker_agent,
    )

    return [retrieve_task, write_task, check_task]
