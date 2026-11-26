
from app.llm import llm

# Import tools
from app.tools.calculator import calculate_fertilizer
from app.tools.crop_info import get_crop_information

# Import system prompt
from app.prompts import farmer_prompt

# Import database functions
from app.database import (
    initialize_database,
    save_message,
    get_chat_history
)

# Import LangChain messages
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)


# =====================================
# 1. REGISTER AVAILABLE TOOLS
# =====================================

tools = [
    calculate_fertilizer,
    get_crop_information
]


# =====================================
# 2. CREATE TOOL LOOKUP DICTIONARY
# =====================================

tools_by_name = {
    tool.name: tool
    for tool in tools
}


# =====================================
# 3. CONNECT TOOLS WITH GROQ AI
# =====================================

llm_with_tools = llm.bind_tools(tools)


# =====================================
# 4. MAIN AI AGENT FUNCTION
# =====================================

def ask_farmer(question, chat_history):

    # Load system prompt and conversation history
    messages = list(
        farmer_prompt.invoke({
            "question": question,
            "chat_history": chat_history
        }).messages
    )

    max_iterations = 5

    for _ in range(max_iterations):

        # Ask AI
        ai_response = llm_with_tools.invoke(messages)

        messages.append(ai_response)

        # Check whether AI wants to use tools
        if not ai_response.tool_calls:
            return ai_response.content

        # Execute selected tools
        for tool_call in ai_response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            selected_tool = tools_by_name.get(tool_name)

            if selected_tool is None:

                result = f"Unknown tool: {tool_name}"

            else:

                try:
                    result = selected_tool.invoke(tool_args)

                except Exception as error:
                    result = f"Tool execution failed: {error}"

            print(f"\nTool Used: {tool_name}")
            print(f"Tool Result: {result}")

            # Send result back to AI
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

    return "I could not complete your request within the tool-call limit."


# =====================================
# 5. RUN SMART FARMER AI APPLICATION
# =====================================

if __name__ == "__main__":

    # Initialize SQLite database
    initialize_database()

    # Demo farmer ID
    farmer_id = "farmer_001"

    # Load previous conversation
    chat_history = []

    saved_messages = get_chat_history(farmer_id)

    for role, content in saved_messages:

        if role == "human":

            chat_history.append(
                HumanMessage(content=content)
            )

        elif role == "ai":

            chat_history.append(
                AIMessage(content=content)
            )

    print("=" * 45)
    print("       SMART FARMER AI ASSISTANT")
    print("=" * 45)

    print(f"Welcome, {farmer_id}!")
    print("Previous conversation loaded.")
    print("Type 'exit' to stop.\n")

    # Start chatbot loop
    while True:

        question = input("Farmer: ")

        if question.lower().strip() == "exit":

            print("Goodbye! Happy farming!")
            break

        if not question.strip():
            continue

        # Get AI response
        answer = ask_farmer(question, chat_history)

        print("\nSmart Farmer AI:")
        print(answer)

        # Update session memory
        chat_history.append(
            HumanMessage(content=question)
        )

        chat_history.append(
            AIMessage(content=answer)
        )

        # Save messages to SQLite
        save_message(farmer_id, "human", question)

        save_message(farmer_id, "ai", answer)
