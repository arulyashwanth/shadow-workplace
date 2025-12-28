from fastapi import APIRouter
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel

class InvokeRequest(BaseModel):
    prompt: str

def create_api_router(graph: CompiledGraph):
    router = APIRouter()

    @router.post("/invoke")
    async def invoke_agent(request: InvokeRequest):
        # The initial state for the graph
        initial_state = {"messages": [request.prompt]}
        result = graph.invoke(initial_state)
        return {"status": "success", "result": result}

    return router
