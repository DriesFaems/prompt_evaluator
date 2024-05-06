import os
import streamlit as st
from groq import Groq

# Set up API key
groq_api_key = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = groq_api_key

# Initialize Groq client
client = Groq()

# Create a title for the app
st.title("Prompt Evaluator")

# Create a description for the app
st.write(
    """
    This app evaluates student prompts based on a set of grading criteria. 
    The response includes a grade for the prompt, a justification for the grade, 
    and suggestions for improvement. Input a prompt, and then refine it based 
    on the feedback received.
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


# Initialize session state to store prompts
if "prompt_history" not in st.session_state:
    st.session_state["prompt_history"] = []

# Display previous feedback
if st.session_state["prompt_history"]:
    st.write("Previous Feedback:")
    for idx, (prompt, feedback) in enumerate(st.session_state["prompt_history"]):
        st.write(f"Prompt {idx + 1}:")
        st.write(prompt)
        st.write(feedback)
        st.write("")

# Input for prompt
prompt = st.text_input("Enter the prompt you would like to evaluate:")

# Button to evaluate the prompt
if st.button("Evaluate Prompt"):
    feedback = evaluate_prompt(prompt)
    st.write(feedback)
    st.session_state["prompt_history"].append((prompt, feedback))
else:
    st.write("Click the button to evaluate the prompt.")