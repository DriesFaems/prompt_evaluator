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

# Create a description for the app
st.write(
    """
    Welcome to the Prompt Feedback Chatbot! 
    This chatbot evaluates student prompts based on a set of grading criteria.
    Enter your prompt, receive feedback, and continue refining your prompts.
    """
)

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

# Initialize session state to store the conversation history, current prompt, and feedback
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []
if "current_prompt" not in st.session_state:
    st.session_state["current_prompt"] = ""
if "feedback" not in st.session_state:
    st.session_state["feedback"] = ""

# Display previous conversation
if st.session_state["conversation_history"]:
    st.write("Conversation:")
    for entry in st.session_state["conversation_history"]:
        st.write(entry)

# Input for the prompt
prompt_input_label = "Refine your prompt:" if st.session_state["current_prompt"] else "Enter your prompt:"
prompt = st.text_input(prompt_input_label, st.session_state["current_prompt"])

# Button to evaluate the prompt
if st.button("Send"):
    st.session_state["feedback"] = evaluate_prompt(prompt)
    st.session_state["conversation_history"].append(f"You: {prompt}")
    st.session_state["conversation_history"].append(f"Bot: {st.session_state['feedback']}")
    st.session_state["current_prompt"] = ""
    st.write(f"You: {prompt}")
    st.write(f"Bot: {st.session_state['feedback']}")
else:
    st.write("Type a prompt and click 'Send'.")

# Allow the user to input a new optimized prompt
if st.session_state["feedback"]:
    optimized_prompt = st.text_input("Provide an optimized prompt:")
    if st.button("Submit Optimized Prompt"):
        feedback = evaluate_prompt(optimized_prompt)
        st.session_state["conversation_history"].append(f"You: {optimized_prompt}")
        st.session_state["conversation_history"].append(f"Bot: {feedback}")
        st.write(f"You: {optimized_prompt}")
        st.write(f"Bot: {feedback}")


