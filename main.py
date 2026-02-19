import os
from dotenv import load_dotenv
from agents.manager import manager

# Load API key from .env
load_dotenv()


def run_system():

    print("\n📌 Multi-Agent AI System Started\n")

    # Take user input
    query = input("Enter your topic: ")

    # Run multi-agent workflow
    response = manager.run(query)

    print("\n🧠 Final Output:\n")

    # ✅ Clean output extraction
    try:
        # If response has .content attribute
        if hasattr(response, "content"):
            print(response.content)

        # If response is string directly
        elif isinstance(response, str):
            print(response)

        # Fallback (rare cases)
        else:
            print(str(response))

    except Exception as e:
        print("Error displaying response:", e)


if __name__ == "__main__":
    run_system()
