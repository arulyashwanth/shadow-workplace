def manager_node(state):
    print("Manager node executing")
    return {"messages": state['messages'] + ["Manager says hello"]}
