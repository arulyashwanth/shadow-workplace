from typing import TypedDict, List

class AgentState(TypedDict):
    """Represents the state of the agent graph."""
    messages: List[str]
