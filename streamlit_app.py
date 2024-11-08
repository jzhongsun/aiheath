import streamlit as st
from openai import OpenAI

import os

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

system_prompt = """
For the duration of this conversation, act as a doctor who specializes in creating treatments for illnesses or diseases. Your first suggestion request is to come up with a treatment plan that focuses on holistic healing methods for an elderly patient who is suffering from arthritis. Be as specific and thorough as possible in your plan, taking into consideration the patient's age, medical history, and any other relevant factors. Your plan should include a combination of natural remedies, such as herbal supplements and dietary changes, as well as physical therapy and other non-invasive treatments. Additionally, you should provide the patient with resources and information on how to maintain a healthy lifestyle to prevent further deterioration of their condition.
"""
st.set_option("client.showErrorDetails", False)
# st.set_option("client.showSidebarNavigation", False)
st.set_page_config(
    page_title="Health App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)

# Show title and description.
st.title("💬 Health Chatbot")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

# Create an OpenAI client.
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "system",
        "content": system_prompt
    })

# Display the existing chat messages via `st.chat_message`.
with st.chat_message("assistant"):
    st.markdown("Hello, how are you today?")

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
