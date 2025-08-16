from langgraph import State, run_graph
from langgraph.prebuilt import agent_executor_node, supervisor_node
from langchain.chat_models import ChatOpenAI
from langchain_agents import Tool  # hypothetical import

llm = ChatOpenAI(temperature=0)
tools = [Tool(name="my_tool", func=lambda x: "tool result")]

# Define specialist agent nodes
agent_tech = agent_executor_node(llm=llm, tools=tools, name="TechAgent")
agent_med = agent_executor_node(llm=llm, tools=tools, name="MedAgent")

# Supervisor logic: choose tech or med agent based on input
def supervisor_fn(state: State):
    user_query = state["input"]
    if "tech" in user_query.lower():
        return "TechAgent"
    elif "medical" in user_query.lower():
        return "MedAgent"
    return None

supervisor = supervisor_node(supervisor_fn, name="Supervisor")

# Build the graph
graph = (
    State(input="What medical conferences in SF?")
    | supervisor
    | agent_tech
    | agent_med
)

response = run_graph(graph)
print(response)
