from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any  # <--- CHANGED: usage of generic type to avoid import errors

# --- DATA MODELS ---
class InvokeRequest(BaseModel):
    prompt: str

# --- ROUTER FACTORY ---
def create_api_router(graph: Any):  # <--- CHANGED: graph: Any (instead of CompiledGraph)
    router = APIRouter()

    @router.post("/invoke")
    async def invoke_agent(request: InvokeRequest):
        # The initial state for the graph
        # Note: We ensure messages is a list as expected by AgentState
        initial_state = {"messages": [request.prompt]}
        
        # Run the graph synchronously
        result = graph.invoke(initial_state)
        
        return {"status": "success", "result": result}

    return router