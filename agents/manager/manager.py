import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Use the model that works for you
    google_api_key=api_key,
    temperature=0.8 # Higher temperature = More creativity/variety
)

def manager_node(state):
    print("--- MANAGER AGENT STARTED ---")
    
    # Safely get user input
    messages = state.get("messages", [])
    user_input = messages[0] if messages else "I want a coding challenge."
    
    print(f"🧠 Analyzing Request: '{user_input}'")

    # --- THE SMARTER PROMPT ---
    system_prompt = """You are a Senior Technical Product Owner.
    Your goal is to create a realistic, unique 1-day Sprint Plan based *strictly* on the user's request.

    ### INSTRUCTIONS:
    1. **Analyze the Role:** - If user says "Junior", give simple tasks (e.g., "Create function", "Fix bug").
       - If user says "Senior", give complex tasks (e.g., "Optimize algorithm", "Design Pattern", "Concurrency").
       - If user mentions specific tech (e.g., "Machine Learning"), the tasks MUST be about that tech (e.g., "Split Data", "Train Model"), NOT web dev.

    2. **Create 3 Distinct Tickets:**
       - Ticket 1: Setup / Foundation (Specific to the domain).
       - Ticket 2: Core Logic / Algorithm (The hard part).
       - Ticket 3: Testing / Validation (Verification).

    3. **Project Name:** Invent a cool, relevant name (e.g., 'neural-net-v1', 'crypto-bot-alpha').

    4. **Output Format:** JSON ONLY. No markdown. No chatter.

    ### EXAMPLE (DO NOT COPY, JUST REFERENCE FORMAT):
    {
      "project_name": "context_aware_name",
      "tickets": [
        {"id": "1", "title": "Unique Task Name", "body": "Specific details..."},
        {"id": "2", "title": "Unique Task Name", "body": "Specific details..."},
        {"id": "3", "title": "Unique Task Name", "body": "Specific details..."}
      ]
    }
    """

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User Request: {str(user_input)}")
        ])

        print(f"Manager Output: {response.content[:100]}...")
        return {"messages": [response.content]}

    except Exception as e:
        print(f"❌ Manager Error: {e}")
        # Fallback JSON to prevent crash
        fallback = json.dumps({
            "project_name": "emergency_fix",
            "tickets": [{"id": "1", "title": "Error", "body": "AI Generation Failed."}]
        })
        return {"messages": [fallback]}