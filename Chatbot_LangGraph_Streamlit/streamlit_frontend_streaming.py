import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= {'configurable': {'thread_id': 'thread-1'}},
                stream_mode= "messages"
            )
        )

# LangGraph streaming modes:
# - "messages": streams LLM output (message chunks, closest to token streaming) → used for chat UI
# - "values": streams full state after each step → useful for debugging
# - "updates": streams only state changes (diffs) → more efficient tracking
# - "events": streams execution flow (node start/end, tool calls, etc.)
#
# Important:
# These modes do NOT stream the same data differently — they stream different layers of the system.
# Only "messages" relates to LLM output; others are about state and execution.
#
# Note:
# Even "messages" streams chunks, not exact tokens (so output may feel bursty).

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})