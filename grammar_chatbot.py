import streamlit as st
import requests

# ---------- Grammar correction function ----------
def correct_grammar(text):
    url = "https://api.languagetool.org/v2/check"
    params = {
        "text": text,
        "language": "en-US",
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

# ---------- Predefined responses ----------
def get_predefined_response(user_input):
    responses = {
        "who are you": "I am a chatbot designed to help with grammar correction. How can I assist you today?",
        "how are you": "I'm doing great, thanks for asking! How can I help you?",
        "hello": "Hi there! How can I help you today?",
        "bye": "Goodbye! Have a great day!",
    }
    
    # Match lowercase user input with predefined responses
    return responses.get(user_input.lower(), None)

# ---------- Chat UI ----------
def chat_ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style="text-align: right;">
                    <div style="display: inline-block; background-color: #DCF8C6;
                    border-radius: 10px; padding: 10px; margin: 5px; max-width: 80%;">
                        {msg["message"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="text-align: left;">
                    <div style="display: inline-block; background-color: #E5E5E5;
                    border-radius: 10px; padding: 10px; margin: 5px; max-width: 80%;">
                        {msg["message"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Input box in a form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Type a sentence")
        submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        # First check if the input matches a predefined response
        predefined_response = get_predefined_response(user_input)
        
        if predefined_response:
            st.session_state.messages.append({"role": "user", "message": user_input})
            st.session_state.messages.append({"role": "bot", "message": predefined_response})
        else:
            # Otherwise, perform grammar correction
            st.session_state.messages.append({"role": "user", "message": user_input})
            corrected = correct_grammar(user_input)
            st.session_state.messages.append(
                {"role": "bot", "message": f"✅ Corrected: **{corrected}**"}
            )

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

# ---------- Main ----------
def main():
    st.set_page_config(page_title="Grammar Chatbot", layout="centered")
    st.title("📝 Grammar Correction Chatbot")
    chat_ui()

if __name__ == "__main__":
    main()
