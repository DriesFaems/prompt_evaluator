import os
import streamlit as st
from groq import Groq

# Set up API key
groq_api_key = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = groq_api_key

# Initialize Groq client
client = Groq()

# Create a title for the app
st.title("Prompt Feedback Chatbot")

# Function to evaluate the prompt
def evaluate_prompt(prompt):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": """You are an expert in evaluating student prompts. 
                Please execute the following steps for the prompt provided by the student:
                
                Step 1: Grade the prompt of a student on a scale of 0 to 10. 
                The grade should reflect the following grading criteria: 
                - More specific prompts should be graded higher
                - Few shot prompts and chain of thought prompts should be graded higher than zero-shot prompts
                - Prompts that clearly specify the identity of the user and the assistant should be graded higher
                - Prompts that stipulate a clear expected output should be graded higher 
                - Prompts that are written in a friendly and encouraging manner should be graded higher
                
                Step 2: Provide a clear justification of the grade. 
                Explain how the student performed on the different criteria
                
                Step 3: Give the student suggestions on how to improve on specific grading criteria
                """
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    feedback = ""
    for chunk in completion:
        feedback += str(chunk.choices[0].delta.content)
    return feedback

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Enter your prompt:"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    response = evaluate_prompt(prompt)

    # Display assistant response in chat message container
    st.chat_message("assistant").markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})



