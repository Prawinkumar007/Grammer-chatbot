import streamlit as st
import requests

# Function to check grammar using LanguageTool API
def correct_grammar(text):
    url = "https://api.languagetool.org/v2/check"
    params = {
        'text': text,
        'language': 'en-US',
    }
    response = requests.post(url, data=params)
    matches = response.json().get("matches", [])
    
    corrected_text = text
    offset_corrections = sorted(matches, key=lambda x: x['offset'], reverse=True)

    for match in offset_corrections:
        # Replace errors with the suggested corrections
        corrected_text = corrected_text[:match['offset']] + match['replacements'][0]['value'] + corrected_text[match['offset'] + match['length']:]
    
    return corrected_text

# Function to simulate a WhatsApp-like chat interface
def chat_ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Add bot's initial message
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "bot", "message": "Hello! How can I help you today?"})

    # Display conversation
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div style="text-align:right; background-color:#DCF8C6; border-radius:10px; padding:10px;">{msg["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:left; background-color:#E5E5E5; border-radius:10px; padding:10px;">{msg["message"]}</div>', unsafe_allow_html=True)

    # Get user input
    user_input = st.text_input("Type your message:", "")

    if user_input:
        # Show user message
        st.session_state.messages.append({"role": "user", "message": user_input})

        # Process the user's input and get the corrected text
        corrected_text = correct_grammar(user_input)
        
        # Show bot response
        st.session_state.messages.append({"role": "bot", "message": f"Here's the corrected text: {corrected_text}"})

# Streamlit app
def main():
    st.title("WhatsApp-style Grammar Correction Chatbot")
    chat_ui()

if __name__ == "__main__":
    main()
