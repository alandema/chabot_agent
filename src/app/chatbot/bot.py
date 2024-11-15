from langchain_google_genai import ChatGoogleGenerativeAI
from .tools.my_tools import get_currency
from langgraph.graph import START, MessagesState, StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages.tool import ToolMessage

from dotenv import load_dotenv
load_dotenv('config.env')

workflow = StateGraph(state_schema=MessagesState)

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    max_tokens=500,
    timeout=None,
    max_retries=2
)

tools = [get_currency]
llm_with_tools = model.bind_tools(tools)

def process_query(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])

    for tool_call in response.tool_calls:
        selected_tool = globals()[tool_call["name"].lower()]
        result = selected_tool.invoke(tool_call['args'])

        tool_message = ToolMessage(
            content=result,
            name=tool_call['name'],
            tool_call_id=tool_call['id'],
        )
        state.append(tool_message)

    return {"messages": response}

workflow.add_edge(START, "model")
workflow.add_node("model", process_query)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

def get_completion(msg, session_id):
    config = {"configurable": {"thread_id": session_id}}
    input_messages = [HumanMessage(msg)]
    response = app.invoke({"messages": input_messages}, config)
    return response["messages"][-1].content

