import os
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=api_key,
    temperature=0.7
)

# --- HELPER: ROBUST JSON EXTRACTOR ---
def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match: return match.group(0)
        return text
    except: return text

def manager_node(state):
    print("--- MANAGER AGENT STARTED ---")
    messages = state.get("messages", [])
    user_input = messages[0] if messages else "I want a coding challenge."
    print(f"🧠 Analyzing Request: '{user_input}'")

    system_prompt = """You are a Senior Technical Mentor.
    Your goal is to generating a coding project tailored EXACTLY to the user's skill level.

    ### 1. DETECT SKILL LEVEL (CRITICAL):
    
    * **LEVEL 1: BEGINNER / FROM SCRATCH / LEARNING**
        * **Keywords:** "Learn", "Scratch", "Beginner", "Newbie", "Basics".
        * **Scope:** 2 Missions. Extremely granular.
        * **Focus:** Syntax, Variables, Printing, Basic Logic.
        * **Tone:** Encouraging Guide.
        * **Example Task:** "Mission 1: Hello World. Create a file and print a string."

    * **LEVEL 2: JUNIOR / ENTRY-LEVEL / INTERNSHIP**
        * **Keywords:** "Internship", "Junior", "Portfolio", "Project", "Build".
        * **Scope:** 3-4 Missions. Functional features.
        * **Focus:** APIs, Database connections, CSS styling, Bug fixes.
        * **Tone:** Engineering Manager.
        * **Example Task:** "Mission 1: API Setup. Connect the frontend to the backend endpoint."

    * **LEVEL 3: SENIOR / ADVANCED / REAL WORLD**
        * **Keywords:** "Advanced", "Scalable", "System Design", "Microservices", "Senior".
        * **Scope:** 4-5 Missions. Complex Architecture.
        * **Focus:** Docker, Caching (Redis), Concurrency, Security, Optimization.
        * **Tone:** CTO / Staff Engineer.
        * **Example Task:** "Mission 1: Containerization. Dockerize the legacy service to reduce deployment drift."

    ### 2. FORMATTING & SAFETY:
    * **Professional Mission Style:** Use titles like "Mission 1: [Task Name]". Explain the 'Why' (Context).
    * **NO DOUBLE QUOTES INSIDE STRINGS.** Use single quotes. (e.g. "body": "Use 'print()' function")
    * **OUTPUT PURE JSON ONLY.**

    ### 3. OUTPUT FORMAT (JSON):
    {
      "project_name": "project-slug",
      "tickets": [
        {
          "id": "1", 
          "title": "🧱 Mission 1: [Task Name]", 
          "body": "**Objective:** [One sentence goal].\\n\\n**Context:** [Why this matters].\\n\\n**Orders:**\\n- [ ] Step 1\\n- [ ] Step 2"
        }
      ],
      "starter_files": [
        { "name": "main.py", "content": "print('Ready')" }
      ]
    }
    """

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User Request: {str(user_input)}")
        ])
        
        clean_content = extract_json(response.content)
        parsed_json = json.loads(clean_content)
        return {"messages": [json.dumps(parsed_json)]}

    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        # Robust Fallback
        fallback = json.dumps({
            "project_name": "shadow-fallback",
            "tickets": [{"id": "1", "title": "Mission 1: System Check", "body": "AI Generation Failed. Please try a simpler prompt."}],
            "starter_files": []
        })
        return {"messages": [fallback]}

    except Exception as e:
        print(f"❌ Manager Crash: {e}")
        return {"messages": ["Error"]}