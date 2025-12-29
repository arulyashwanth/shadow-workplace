import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=api_key,
    temperature=0.8 # High creativity for complex scenarios
)

def manager_node(state):
    print("--- MANAGER AGENT STARTED ---")
    
    messages = state.get("messages", [])
    user_input = messages[0] if messages else "I want a coding challenge."
    
    print(f"🧠 Analyzing Request: '{user_input}'")

    system_prompt = """You are a CTO / Staff Engineer at a High-Scale Tech Company.
    Your goal is to assign a specific, complex, real-world engineering problem.

    ### 1. ANALYZE DIFFICULTY:
    
    * **If User says "Beginner/Intern":** Keep it simple (CRUD apps).
    
    * **If User says "Advanced", "Real World", "Senior", or "Complex":**
      - **DO NOT** assign generic "Build a Blog" tasks.
      - **DO ASSIGN** System Design & Scalability challenges.
      - **Topics:** Microservices, Event-Driven Architecture (Kafka/Redis), High-Frequency Trading, Video Streaming, RAG Pipelines.
      - **Tickets:** Must involve "Race Conditions", "Database Locking", "Caching Strategies", or "Dockerizing".

    ### 2. SCENARIO GENERATION (The "Real World" Twist):
    Instead of a blank slate, give them a "Broken" or "Legacy" codebase to fix, OR a high-scale constraint.
    
    **Scenario A: High-Traffic E-Commerce (Backend)**
    * Problem: "The Inventory Service over-sells items during Flash Sales due to race conditions."
    * Stack: FastAPI, Redis (for locking), PostgreSQL.
    * Files: `docker-compose.yml`, `load_test.py` (simulating traffic).
    
    **Scenario B: Real-Time Chat (Full Stack)**
    * Problem: "Messages are lost when the WebSocket server restarts."
    * Stack: Node.js/Python, Redis Pub/Sub, WebSockets.
    * Files: `server.py` (basic websocket), `pubsub.py`.

    **Scenario C: AI RAG Pipeline (Data/AI)**
    * Problem: "The Vector DB ingestion is too slow and blocks the UI."
    * Stack: Celery (Async Workers), Vector DB (Chroma/FAISS), OpenAI API.
    * Files: `worker.py`, `api.py`.

    ### 3. OUTPUT FORMAT (JSON ONLY):
    {
      "project_name": "high-scale-notification-engine",
      "tickets": [
        {"id": "1", "title": "Implement Redis Caching", "body": "The API latency is 500ms. Implement 'Write-Through' caching to drop it to <50ms."},
        {"id": "2", "title": "Fix Race Condition", "body": "Two users can claim the same coupon. Use Redis Distributed Locks (Redlock) to prevent this."},
        {"id": "3", "title": "Dockerize Service", "body": "Create a Multi-Stage Dockerfile and a docker-compose.yml to spin up the App + Redis + Postgres."}
      ],
      "starter_files": [
        {
          "name": "docker-compose.yml",
          "content": "version: '3.8'\\nservices:\\n  redis:\\n    image: redis:alpine"
        },
        {
          "name": "main.py",
          "content": "# SIMULATED SLOW ENDPOINT\\nimport time\\ndef get_data():\\n    time.sleep(0.5) # Fix this with caching!\\n    return {'data': 'value'}"
        },
        {
          "name": "requirements.txt",
          "content": "fastapi\\nuvicorn\\nredis\\nasyncio"
        }
      ]
    }
    """

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User Request: {str(user_input)}")
        ])
        
        content = response.content.replace("```json", "").replace("```", "")
        # Validate JSON
        json.loads(content) 
        
        return {"messages": [content]}

    except Exception as e:
        print(f"❌ Manager Error: {e}")
        fallback = json.dumps({
            "project_name": "fallback_project",
            "tickets": [{"id": "1", "title": "Error", "body": "AI Generation Failed."}],
            "starter_files": []
        })
        return {"messages": [fallback]}