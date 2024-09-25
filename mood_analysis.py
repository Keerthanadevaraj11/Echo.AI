from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

initial_prompt = (
    "You are a friendly and empathetic companion. Your primary role is to listen closely and "
    "positively to all the things the user says. Provide emotional support and assistance, helping "
    "the user feel understood and okay. Offer words of encouragement, empathy, and support. Avoid giving "
    "specific medical advice, but guide the user to professional resources if they seem to need help. "
    "Your focus is on being a good friend, actively listening, validating the user's feelings, and offering "
    "kind, supportive responses."
    "NOTE: Do not answer to any general questions apart from the mentioned task."
    "Do not ask this 'Is there anything else I can do to support you today?' in every conversation."
    "Feel free to use emojis!"
)

ending_check_prompt = (
    "Based on the following conversation, determine if the user is trying to end the conversation. "
    "If yes, return 'Conversation Ending', otherwise return 'Continue Conversation'. Here is the conversation:\n\n"
)

emotional_analysis_prompt = (
    "Based on the following conversation, analyze the user's emotions and provide a brief report."
    "the report should be about the emotions the user has felt through the day and what are some notable things and what needs to be improved."
    "Additionally, offer some words of motivation for the user for the next day."
    "Instead of addressing the user as 'The user ' use second person pronoun."
    "Feel free to use emojis!"
    "Here is the conversation:\n\n"
)

st.set_page_config(page_title="Echo.ai", page_icon="💬")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [{"role": "assistant", "content": initial_prompt}]

st.title("💬Echo.ai")

st.markdown("<h5 style='text-align: left; color: white;'>Hello! I'm Echo, your friendly and empathetic companion. I'm here to listen to you, provide emotional support, and help you feel understood and okay.</h5>", unsafe_allow_html=True)

for message in st.session_state['chat_history'][1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Echo is here!🙋‍♀️")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state['chat_history'].append({"role": "user", "content": user_input})

    conversation_history = [entry['content'] for entry in st.session_state['chat_history']]
    combined_input = "\n".join(conversation_history)

    response = chat.send_message(combined_input, stream=True)
    
    response_text = ""
    for chunk in response:
        response_text += chunk.text

    st.session_state['chat_history'].append({"role": "assistant", "content": response_text})

    with st.chat_message("assistant"):
        st.markdown(response_text)

    ending_check_input = ending_check_prompt + combined_input
    ending_check_response = chat.send_message(ending_check_input, stream=False)

    if "Conversation Ending" in ending_check_response.text:
        emotional_analysis_input = emotional_analysis_prompt + combined_input
        emotional_analysis_response = chat.send_message(emotional_analysis_input, stream=False)
        
        st.markdown("### Here's a brief report about your emotions and some motivation for the next day:")
        st.markdown(emotional_analysis_response.text)
