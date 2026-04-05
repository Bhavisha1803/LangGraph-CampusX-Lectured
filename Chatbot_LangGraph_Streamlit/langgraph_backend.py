from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
import os
from dotenv import load_dotenv

load_dotenv()

llm = llm =ChatGroq(
    model="llama-3.3-70b-versatile",    
    api_key=os.getenv("GROQ_API_KEY"),
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# stream_generator = chatbot.stream(
#     {"messages": [HumanMessage(content="write a 500 word essay on AI")]},
#     config = {'configurable': {'thread_id': 'thread-1'}},
#     stream_mode="messages"
# )
# print(type(stream_generator))

# for message_chunk,metadata in stream_generator:
#     print(message_chunk.content, end = '', flush=True)
# this is used to stream the response, using generator and graph.stream() method. The stream_mode is set to "messages" which means that the response will be streamed as messages. The for loop iterates over the stream_generator and prints the content of each message chunk as it is received.