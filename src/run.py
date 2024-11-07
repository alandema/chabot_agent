# from app.interface import main
from typing import TypedDict, Literal, Annotated
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages, AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState
load_dotenv('config.env')

# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]

class MessagesState(MessagesState):
    pass

def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph = builder.compile()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

llm_with_tools = llm.bind_tools([multiply])



def main(message, id="abc123"):
    output = graph.invoke({"messages": [HumanMessage(message)]}, config={"configurable": {"thread_id": id}})
    print(output)

if __name__ == '__main__':

    # main.app.run(debug=True)
    main("Hello!", id="abc123")
