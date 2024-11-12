# from app.interface import main
from typing import TypedDict, Literal, Annotated
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
load_dotenv('config.env')
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages, AnyMessage, ToolMessage
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import MemorySaver

class TypedDictState(TypedDict):
    messages: list
    name: str
    mood: Literal["happy","sad"]

def node_1(state):
    print("---Node 1---")
    return {"name": state['name'] + " is ... "}

def node_2(state):
    print("---Node 2---")
    return {"mood": "happy"}

def node_3(state):
    print("---Node 3---")
    return {"mood": "sad"}

class UserName(TypedDict):
    name: str




def decide_mood(state) -> Literal["node_2", "node_3"]:
        
    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return "node_2"
    
    # 50% of the time, we return Node 3
    return "node_3"

# Build graph
builder = StateGraph(TypedDictState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful and polite assistant",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
llm_oputput = llm.with_structured_output(UserName)
chain = prompt | llm


def main(message, id="abc123"):
    output = graph.invoke({"messages": message}, config={"configurable": {"thread_id": id}})

    for message in output["messages"]:
        if isinstance(message, AIMessage):
            print(message.content)

if __name__ == '__main__':

    # main.app.run(debug=True)
    for messages in ['Hello, my name is Alan.']:
        main(messages, id="abc123")
