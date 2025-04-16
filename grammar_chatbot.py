import streamlit as st
import requests

# Grammar correction using LanguageTool API
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
    for offset, length, replacement in corrections:
        text = text[:offset] + replacement + text[offset + length:]

    return text

# Chat UI
def chat_ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

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

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Type your sentence")
        submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        st.session_state.messages.append({"role": "user", "message": user_input})
        corrected = correct_grammar(user_input)
        st.session_state.messages.append({
            "role": "bot",
            "message": f"✅ Here's the corrected version:\n\n**{corrected}**"
        })
        # ❌ No more experimental_rerun()

# Main
def main():
    st.set_page_config(page_title="Grammar Chatbot", layout="centered")
    st.title("📝 Grammar Correction Chatbot")
    chat_ui()

if __name__ == "__main__":
    main()
