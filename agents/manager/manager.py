import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# FORCE LOAD: Load .env file explicitly to avoid "KeyError"
load_dotenv()

# DEBUG: Print to terminal to prove the key exists
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ CRITICAL ERROR: GOOGLE_API_KEY is missing from environment!")
else:
    print(f"✅ Manager Agent found API Key: {api_key[:5]}...")

# 1. Initialize Gemini with the safe key
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key, 
    temperature=0.7
)

def manager_node(state):
    print("--- MANAGER AGENT STARTED ---")
    
    # 2. Get User Input
    # Safely get the first message. If state is empty, use a default.
    messages = state.get("messages", [])
    if messages:
        user_input = messages[0]
    else:
        user_input = "I want a random coding task."
    
    # 3. The Logic (Prompt)
    system_prompt = """You are a Senior Product Owner. 
    Your goal: Create a realistic 1-day Hackathon Sprint for a user.
    
    Rules:
    1. Create exactly 3 technical tasks.
    2. OUTPUT MUST BE VALID JSON ONLY.
    
    JSON Format:
    {
      "project_name": "library_system",
      "tickets": [
        {"id": "1", "title": "Setup FastAPI", "body": "Initialize app."},
        {"id": "2", "title": "DB Config", "body": "Setup SQLite."}
      ]
    }
    """

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=str(user_input))
        ])
        print(f"Manager Generated: {response.content}")
        return {"messages": [response.content]}
        
    except Exception as e:
        print(f"❌ Manager AI Failed: {e}")
        # Return a fallback JSON so the next agent doesn't crash
        fallback_json = json.dumps({
            "project_name": "backup_project",
            "tickets": [{"id": "0", "title": "Error", "body": "AI failed to generate."}]
        })
        return {"messages": [fallback_json]}