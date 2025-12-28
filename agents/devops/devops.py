import json

def devops_node(state):
    """
    The GitOps Agent: Reads the Manager's plan and 'builds' the infrastructure.
    """
    print("--- DEVOPS AGENT STARTED ---")
    
    # 1. Read the Manager's output (the last message in the list)
    manager_output = state["messages"][-1]
    
    # Clean up the output (sometimes AI adds ```json ... ``` wrappers)
    clean_json = manager_output.replace("```json", "").replace("```", "").strip()
    
    try:
        sprint_plan = json.loads(clean_json)
        repo_name = sprint_plan.get("project_name", "shadow-project")
        
        # --- MOCK GITHUB ACTION (Real API call goes here later) ---
        result_msg = f"✅ DevOps Action: Created GitHub Repo '{repo_name}' with {len(sprint_plan['tickets'])} issues."
    except Exception as e:
        result_msg = f"❌ DevOps Error: Could not parse Manager's plan. Error: {str(e)}"

    print(result_msg)
    
    return {"messages": [result_msg]}