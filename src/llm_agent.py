import json
import os
from tools.my_tools import get_currency
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
load_dotenv('config.env')

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages.tool import ToolMessage


SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    max_tokens=500,
    timeout=None,
    max_retries=2,
    safety_settings=SAFETY_SETTINGS
)

trimmer = trim_messages(
    max_tokens=500,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

workflow = StateGraph(state_schema=MessagesState)

# Define the function that calls the model


def call_model(state: MessagesState):
    chain = prompt | llm_with_tools
    trimmed_messages = trimmer.invoke(state["messages"])

    response = chain.invoke(trimmed_messages)
    trimmed_messages.append(response)

    for tool_call in response.tool_calls:
        selected_tool = {"get_currency": get_currency}[tool_call["name"].lower()]
        result = selected_tool(**tool_call['args'])

        tool_message = ToolMessage(
            content=result,
            name=tool_call['name'],
            tool_call_id=tool_call['id'],
        )
        trimmed_messages.append(tool_message)

    response = chain.invoke(trimmed_messages)

    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in Brazilian portuguese.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

tools = [get_currency]

llm_with_tools = model.bind_tools(tools)


def main(input, id):
    config = {"configurable": {"thread_id": id}}
    input_messages = [HumanMessage(input)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()  # output contains all messages in state
    # for chunk, metadata in app.stream(
    #     {"messages": input_messages},
    #     config,
    #     stream_mode="messages",
    # ):
    #     if isinstance(chunk, AIMessage):  # Filter to just model responses
    #         print(chunk.content, end="")


if __name__ == "__main__":
    for message in ["Hello, my name is Alan and I would like to convert 800 euros to USD on 2024-09-25"]:
        main(message, id="abc123")
