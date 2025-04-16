import streamlit as st
import requests

# ✅ Improved grammar correction using LanguageTool API
def correct_grammar(text):
    url = "https://api.languagetool.org/v2/check"
    params = {
        'text': text,
        'language': 'en-US',
    }
    response = requests.post(url, data=params)
    matches = response.json().get("matches", [])

    corrections = []
    for match in matches:
        if match["replacements"]:
            offset = match["offset"]
            length = match["length"]
            replacement = match["replacements"][0]["value"]
            corrections.append((offset, length, replacement))

    corrections.sort(reverse=True)

    corrected_text = text
    for offset, length, replacement in corrections:
        corrected_text = corrected_text[:offset] + replacement + corrected_text[offset + length:]

    return corrected_text

# ✅ WhatsApp-style chatbot UI
def chat_ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "bot", "message": "👋 Hello! Type a sentence and I’ll correct its grammar."})

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div style="text-align:right; background-color:#DCF8C6; border-radius:10px; padding:10px; margin:5px;">{msg["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:left; background-color:#E5E5E5; border-radius:10px; padding:10px; margin:5px;">{msg["message"]}</div>', unsafe_allow_html=True)

    # Chat input box
    user_input = st.text_input("💬 Type your sentence here", key="input")

    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "message": user_input})

        # Get corrected text
        corrected = correct_grammar(user_input)

        # Append bot message
        st.session_state.messages.append({"role": "bot", "message": f"✅ Here's the corrected version:\n\n**{corrected}**"})

        # Clear input for next message
        st.session_state.input = ""

        # Rerun to refresh the chat
        st.experimental_rerun()

# ✅ Streamlit app entry point
def main():
    st.set_page_config(page_title="Grammar Chatbot", layout="centered")
    st.title("📝 Grammar Correction Chatbot (WhatsApp Style)")
    chat_ui()

if __name__ == "__main__":
    main()
