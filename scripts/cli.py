"""Simple CLI for local testing outside Streamlit."""

from smart_book_qa.crew import run_crew


def main() -> None:
    print("=" * 50)
    print("  Smart Book Q&A Crew")
    print("  Local CLI")
    print("=" * 50)
    print()
    print("Build the vector index from the Streamlit app before using this script.")
    print("Type 'quit' to exit.")
    print()

    while True:
        question = input("Your question: ").strip()

        if question.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        if not question:
            print("Please type a question.\n")
            continue

        print("\nThe crew is working on your question...\n")
        result = run_crew(question)

        print()
        print("=" * 50)
        print("  FINAL ANSWER:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        print()


if __name__ == "__main__":
    main()
