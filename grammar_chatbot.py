import streamlit as st
import requests

# ✅ Function to correct grammar using LanguageTool API
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

    # Sort by offset in reverse to avoid messing up string indices
    corrections.sort(reverse=True)

    corrected_text = text
    for offset, length, replacement in corrections:
        corrected_text = corrected_text[:offset] + replacement + corrected_text[offset + length:]

    return corrected_text

# ✅ Chat UI with WhatsApp-style bubbles
def chat_ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "bot", "message": "👋 Hello! Type a sentence and I’ll correct its grammar."})

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'''
                <div style="text-align:right;">
                    <div style="display:inline-block; background-color:#DCF8C6; border-radius:10px; padding:10px; margin:5px; max-width:80%;">
                        {msg["message"]}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div style="text-align:left;">
                    <div style="display:inline-block; background-color:#E5E5E5; border-radius:10px; padding:10px; margin:5px; max-width:80%;">
                        {msg["message"]}
                    </div>
                </div>
            ''', unsafe_allow_html=True)

    # Input box
    user_input = st.text_input("💬 Type your sentence here", key="user_input")

    if user_input:
        # Add user's message
        st.session_state.messages.append({"role": "user", "message": user_input})

        # Get corrected text
        corrected = correct_grammar(user_input)

        # Add bot's response
        st.session_state.messages.append({"role": "bot", "message": f"✅ Here's the corrected version:\n\n**{corrected}**"})

        # Clear input
        st.session_state.user_input = ""

        # Trigger rerun to update UI
        st.experimental_rerun()

# ✅ Main app function
def main():
    st.set_page_config(page_title="Grammar Chatbot", layout="centered")
    st.title("📝 Grammar Correction Chatbot")
    chat_ui()

if __name__ == "__main__":
    main()
