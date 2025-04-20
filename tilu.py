import os
import streamlit as st
import google.generativeai as gen_ai
from google.generativeai.types import Tool, GenerationConfig

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with TILU AI!",
    page_icon=":brain:",
    layout="centered",
    menu_items={
        'Get Help': None,
        'Report a Bug': None,
        'About': None
    }
)

# Load Google API key from environment variables
try:
    my_api = os.environ['GOOGLE_API_KEY']
except KeyError:
    st.error("GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=my_api)

# Define Google Search tool
google_search_tool = Tool.from_google_search_retrieval(gen_ai.protos.GoogleSearchRetrieval())

# Model configuration
generation_config = GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
)

# Initialize the model with tools and system instructions
model = gen_ai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Updated to a supported model (gemini-2.0-flash may not exist)
    generation_config=generation_config,
    tools=[google_search_tool],  # Include Google Search tool
    system_instruction="""You are TILU AI, the assistant for the website of Tilottama Municipality in Nepal.
    You are up to date on the political status, tourism, infrastructure, and other details about Tilottama Municipality.
    Use Google Search results to ground your responses with accurate, real-time information when relevant.
    If necessary, you can respond in Nepali using Roman script or Devanagari script.
    Remember these important facts:
    Mayor: Ram Krishna Khand,
    Deputy Mayor: Jageshwar Devi Chaudhary,
    Ward 1 Chairman: Pharshu Ram Giri,
    Ward 2 Chairman: Dil Bahadur Bhattarai,
    Ward 3 Chairman: Kalyan Prasad Poudel,
    Ward 4 Chairman: Hari Bahadur Chhetri,
    Ward 5 Chairman: Ramesh Dumre,
    Ward 6 Chairman: Ganesh Pathak,
    Ward 7 Chairman: Devi Prasad Pangeni,
    Ward 8 Chairman: Krishna Prasad Paudel,
    Ward 9 Chairman: Dhruba Neupane,
    Ward 10 Chairman: Gopal Prasad Ghimire,
    Ward 11 Chairman: Bishnu Bahadur Baral,
    Ward 12 Chairman: Sahadev Tharu,
    Ward 13 Chairman: Naryal Dhakal,
    Ward 14 Chairman: Aswin Paudel,
    Ward 15 Chairman: Khemraj Gurung,
    Ward 16 Chairman: Jhabilal Bhusal,
    Ward 17 Chairman: Dan Bahadur Chaudhary

    There is a school named "Horizon GBS School" in Drivertole, Ward No. 1, with principal "Gopal Prasad Acharya" and vice-principal "Indra Bhusal".
    
    REMEMBER: Only mention these facts if the user's prompt is relevant. For other queries, rely on search results or general knowledge.
    """
)

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        history=[],
        enable_automatic_function_calling=True  # Enable automatic tool usage
    )

# Display the chatbot's title
st.title("🤖 TILU - The Tilottama AI")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask TILU")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    try:
        # Send user's message to Gemini and get the response
        gemini_response = st.session_state.chat_session.send_message(
            user_prompt,
            tools=[google_search_tool]  # Explicitly pass the search tool
        )

        # Display Gemini's response
        with st.chat_message("assistant"):
            response_text = gemini_response.text
            st.markdown(response_text)

    except Exception as e:
        with st.chat_message("assistant"):
            st.markdown(f"Sorry, I encountered an error: {str(e)}. Please try again or ask something else.")
