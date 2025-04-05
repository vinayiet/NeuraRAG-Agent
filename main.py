from langgraph.graph import StateGraph
from tools.weather_tool import get_weather
from tools.pdf_tool import query_pdf, load_pdf_and_create_vectorstore

vectorstore = load_pdf_and_create_vectorstore('test.pdf')

def decide_action(input):
    if "weather" in input["query"].lower():
        return "weather"
    else:
        return "pdf"

def run_weather_node(state):
    return {"response": get_weather(state["query"])}

def run_pdf_node(state):
    return {"response": query_pdf(vectorstore, state["query"])}

workflow = StateGraph()

workflow.set_entry_point("decision")

workflow.add_node("decision", decide_action)

workflow.add_conditional_edges("decision", lambda s: decide_action(s), {
    "weather": "weather_node",
    "pdf": "pdf_node"
})

workflow.add_node("weather_node", run_weather_node)
workflow.add_node("pdf_node", run_pdf_node)

app = workflow.compile()
