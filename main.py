
from app.llm import llm
from app.prompts import farmer_prompt

from app.tools.calculator import calculate_fertilizer

from app.database import (
    initialize_database,
    save_message,
    get_chat_history
)

from langchain_core.messages import HumanMessage, AIMessage


def main():
    initialize_database()

    # Demo farmer identity
    farmer_id = "farmer_001"

    chat_history = []

    # Load only this farmer's history
    saved_messages = get_chat_history(farmer_id)

    for role, content in saved_messages:
        if role == "human":
            chat_history.append(HumanMessage(content=content))
        elif role == "ai":
            chat_history.append(AIMessage(content=content))

    chain = farmer_prompt | llm

    print("SMART FARMER AI ASSISTANT")
    print(f"Farmer ID: {farmer_id}")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("Farmer: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        response = chain.invoke({
            "question": question,
            "chat_history": chat_history
        })

        print("\nSmart Farmer AI:")
        print(response.content)

        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=response.content))

        save_message(farmer_id, "human", question)
        save_message(farmer_id, "ai", response.content)


if __name__ == "__main__":
    main()
