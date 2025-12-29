from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# Import Agents
from agents.manager.manager import manager_node
from agents.devops.devops import devops_node
from agents.senior_dev.senior_dev import senior_dev_node
from agents.security.security import security_node 

app = FastAPI()

# --- WORKFLOW 1: SETUP (Get Hired) ---
class SetupState(TypedDict):
    messages: List[str]

setup_workflow = StateGraph(SetupState)
setup_workflow.add_node("manager", manager_node)
setup_workflow.add_node("devops", devops_node)
setup_workflow.set_entry_point("manager")
setup_workflow.add_edge("manager", "devops")
setup_workflow.add_edge("devops", END)
setup_graph = setup_workflow.compile()

# --- WORKFLOW 2: REVIEW (The Security Pipeline) ---
class ReviewState(TypedDict):
    repo_url: str
    messages: List[str]
    security_status: str 

review_workflow = StateGraph(ReviewState)
review_workflow.add_node("security", security_node)
review_workflow.add_node("senior_dev", senior_dev_node)

# 1. Start at Security
review_workflow.set_entry_point("security")

# 2. Define Logic: Stop if blocked, Continue if clean
def route_security(state):
    status = state.get("security_status", "clean")
    if status == "blocked":
        return "end"       # Blocked! Stop here.
    return "senior_dev"    # Clean! Go to roast.

# 3. Add the Conditional Edge
review_workflow.add_conditional_edges(
    "security",
    route_security,
    {
        "end": END,
        "senior_dev": "senior_dev"
    }
)

review_workflow.add_edge("senior_dev", END)
review_graph = review_workflow.compile()

# --- API ENDPOINTS ---

class PromptInput(BaseModel):
    prompt: str

@app.post("/agent/start_job")
async def start_job(input: PromptInput):
    """Triggers Manager -> DevOps"""
    initial_state = {"messages": [input.prompt]}
    result = setup_graph.invoke(initial_state)
    return result

class ReviewInput(BaseModel):
    repo_url: str

@app.post("/agent/review_code")
async def review_code(input: ReviewInput):
    """Triggers Security -> Senior Dev"""
    # Initialize with status='clean' just in case
    initial_state = {
        "repo_url": input.repo_url, 
        "messages": [], 
        "security_status": "clean"
    }
    result = review_graph.invoke(initial_state)
    return result

@app.get("/")
def read_root():
    return {
        "status": "Shadow Workplace is Online", 
        "routes": ["/agent/start_job", "/agent/review_code"]
    }