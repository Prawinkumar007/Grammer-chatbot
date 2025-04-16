import streamlit as st
import language_tool_python

# Initialize the language tool
tool = language_tool_python.LanguageTool('en-US')

def correct_grammar(text):
    # Check the text for errors
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

# Streamlit app
def main():
    st.title("Grammar Correction Chatbot")
    
    # User input
    user_input = st.text_area("Type your text here:", "")
    
    if user_input:
        corrected_text = correct_grammar(user_input)
        st.subheader("Corrected Text")
        st.write(corrected_text)

if __name__ == "__main__":
    main()
