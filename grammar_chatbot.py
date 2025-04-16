import streamlit as st
import language_tool_python

# Initialize the language tool
tool = language_tool_python.LanguageTool('en-US')

st.title("Grammar Correction Bot")
st.write("Hello! How can I help you today?")

# User input
user_input = st.text_input("Enter a sentence to correct:")

# Check grammar and suggest corrections
if user_input:
    matches = tool.check(user_input)
    corrected_text = language_tool_python.utils.correct(user_input, matches)
    
    # Output original and corrected sentence
    st.write("### Original:")
    st.write(user_input)
    
    st.write("### Corrected:")
    st.success(corrected_text)
