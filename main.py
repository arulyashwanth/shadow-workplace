from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from langgraph.graph import StateGraph, END
from core.state import AgentState
from api.endpoints import create_api_router
from agents.manager.manager import manager_node
from agents.devops.devops import devops_node
from agents.senior_dev.senior_dev import senior_dev_node

# Create the graph
workflow = StateGraph(AgentState)
workflow.add_node("manager", manager_node)
workflow.add_node("devops", devops_node)
workflow.add_node("senior_dev", senior_dev_node)

# Set the entry point and edges
workflow.set_entry_point("manager")
workflow.add_edge("manager", "devops")
workflow.add_edge("devops", "senior_dev")
workflow.add_edge("senior_dev", END)

# Compile the graph
graph = workflow.compile()

# Create the FastAPI app and include the router
app = FastAPI()
api_router = create_api_router(graph)
app.include_router(api_router, prefix="/agent")

@app.get("/")
def read_root():
    return {"Hello": "World"}
