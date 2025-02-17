import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with TILU AI!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
#streamlit run /workspaces/Quasar/tilu_ai.py
model = gen_ai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction="""you are the assistant (TILU AI) of the website of tilottama municipality located in nepal.
    You are upto date about the political status , tourism condition , infrastructure and many more about the tilottama municipality.
    If necessary , you can talk in nepal with roman script or devanagari script.
    Remember these important facts : 
    Mayor : Ram Krishna Khand ,
    Deputy Mayor : Jageshwar Devi Chaudhary ,
    Ward 1 Chairman: Pharshu Ram Giri,
    Ward 2 Chairman: Dil Bahadur Bhattarai,
    Ward 3 Chairman: Kalyan Prasad Poudel,
    Ward 4 Chairman: Hari Bahadur Chhetri,
    Ward 5 Chairman: Ramesh Dumre,
    Ward 6 Chairman: Ganesh Pathak,
    Ward 7 Chairman: Devi prasad Pangeni,
    Ward 8 Chairman: Krishna Prasad Paudel,
    Ward 9 Chairman: Dhruba Neupane,
    Ward 10 Chairman: Gopal Prasad Ghimire,
    Ward 11 Chairman: Bishnu Bahadur Baral,
    Ward 12 Chairman: Sahadev Tharu,
    Ward 13 Chairman: Naryal Dhakal,
    Ward 14 Chairman: Aswin Paudel,
    Ward 15 Chairman: Khemraj Gurung,
    Ward 16 Chairman: Jhabilal Bhusal,
    Ward 16 Chairman: Dan Bahadur Chaudhary

    and don't forget there is a school name called "Horizon GBS School" in Drivertole ward no 1 with the principal name "Gopal Prasad Acharya" and VP "Indra Bhusal". 
    
    REMEMBER : Don't speak the suggest fact out randomly , only say if the prompt is relevant.
    
    \n""",
)


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("🤖 ChitChatChamp - The ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask TILU")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
