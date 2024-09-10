import os
import streamlit as st
from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

def chat_with_groq(prompt, conversation_history=[]):
    system_message = {
        "role": "system",
        "content": "You are an AI Programming Tutor specializing in Python, AI, and ML. Provide concise, accurate answers with code examples when relevant."
    }
    messages = [system_message] + conversation_history + [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
        max_tokens=1000,
        temperature=0.7
    )
    
    return response.choices[0].message.content

# Streamlit app
st.title("AI Programming Tutor")

# Initialize session state for conversation history and input key
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Display conversation history
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.write("You: " + message["content"])
    else:
        st.write("Tutor: " + message["content"])

# User input
user_input = st.text_input("Ask me anything about programming, AI, or ML:", key=f"user_input_{st.session_state.input_key}")

if st.button("Send"):
    if user_input:
        # Add user message to conversation history
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        
        # Get chatbot response
        with st.spinner("Thinking..."):
            response = chat_with_groq(user_input, st.session_state.conversation_history)
        
        # Add chatbot response to conversation history
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        
        # Increment the input key to reset the text input
        st.session_state.input_key += 1
        
        # Rerun the app to update the display
        st.rerun()

# Add a button to clear the conversation
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.session_state.input_key += 1
    st.rerun()

# Sidebar with learning resources
st.sidebar.title("Learning Resources")
st.sidebar.markdown("""
- [Python Documentation](https://docs.python.org/3/)
- [Machine Learning Course](https://www.coursera.org/learn/machine-learning)
- [AI for Everyone](https://www.coursera.org/learn/ai-for-everyone)
""")