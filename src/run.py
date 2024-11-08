# from app.interface import main
from typing import TypedDict, Literal, Annotated
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages, AnyMessage, ToolMessage
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import MemorySaver
load_dotenv('config.env')

memory = MemorySaver()
# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]

class MessagesState(MessagesState):
    pass

def tool_calling_llm(state: MessagesState):
    return {"messages": [chain.invoke(state["messages"])]}

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def add(a: int, b: int) -> int:
    """Sum a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply, add]))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)

graph = builder.compile(checkpointer=memory)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


llm_with_tools = llm.bind_tools([multiply, add])

prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful and polite assistant",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | llm_with_tools


def main(message, id="abc123"):
    output = graph.invoke({"messages": message}, config={"configurable": {"thread_id": id}})

    for message in output["messages"]:
        if isinstance(message, AIMessage):
            print(message.content)

if __name__ == '__main__':

    # main.app.run(debug=True)
    for messages in ['Hello, my name is Alan.','Sum 3 plus 5', 'now multiply by 2']:
        main(messages, id="abc123")
