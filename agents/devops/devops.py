def devops_node(state):
    print("DevOps node executing")
    return {"messages": state['messages'] + ["DevOps says hello"]}
