from groq import Groq
import os
import tomllib
import streamlit as st


groq_api_key = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = groq_api_key

# ask user to input the initial prompt

prompt = st.text_input("Enter the prompt you would like to evaluate:")

# create click button to start

if st.button('Evaluate Prompt'):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in evaluating student prompts. \n\nPlease execute the following steps for the prompt provided by the student:\n\nStep 1: Grade the prompt of a student on a scale of 0 to 10. The grade should reflect the following grading criteria: \nCriterium 1: More specific prompts should be graded higher\nCriterium 2: Few shot prompts and chain of thought prompts should be graded higher than zero-shot prompts\nCriterium 3: Prompts that clearly specify the identity of the user and the assistant should be graded higher\nCriterium 4: prompts that stipulate a clear expected output should be graded higher \nCriterium 5: prompts that are written in a friendly and encouraging manner should be graded higher\nStep 2: Provide a clear justification of the grade. Explain how the student performed on the different criteria\nStep 3:  Give the student suggestions on how to improve on specific grading criteria\n"
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    text = ""
    for chunk in completion:
        text = text + str(chunk.choices[0].delta.content)
    st.write(text)
else:
    st.write('Click the button to evaluate the prompt')