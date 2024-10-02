import streamlit as st # for the frontend
from langchain_community.llms import Ollama 
import logging
import pathlib

# Initialize logging
logging.basicConfig(filename='chatbot_errors.log', level=logging.ERROR)
#chat history file inserting

#ollama initialize
llama = Ollama(model="llama3.1")

st.title("MK's chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Enter your message:"):
    # Validate input
    if len(prompt.strip()) < 1:
        st.error("Please enter a valid message.")
    else:
        # Process input
        prompt = prompt.lower()
        prompt = ''.join(e for e in prompt if e.isalnum() or e.isspace())

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f"**You:** {prompt}")


        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Save conversation to file
        with open("convo.txt", "a") as file:
            file.write(f"User: {prompt}\n")

        # Generate assistant response using LLaMA 3
        try:
            with st.spinner("Generating response..."):
                response = llama.invoke(prompt)
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            st.error(f"Error generating response: {str(e)}")
        else:
            if response:
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(f"**MK's chatbot:** {response}")

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                with open("convo.txt", "a") as file:
                    file.write(f"assistant: {response}\n")
                # Limit conversation history
                if len(st.session_state.messages) > 100:
                    st.session_state.messages = st.session_state.messages[-100:]
            else:
                st.error("Assistant response is empty.")
