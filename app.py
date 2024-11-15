import streamlit as st
import os
from groq import Groq
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF
import time
st.set_page_config(page_title="AI Smart Study Assistant", page_icon="📚", layout="wide")

# Set the page state
if "page" not in st.session_state:
    st.session_state.page = "main"

# Navigation logic
if st.session_state.page == "main":
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Register"):
            st.session_state.page = "register"

    with col2:
        if st.button("Login"):
            st.session_state.page = "login"
# Initialize session state for storing inputs and responses
if 'text_responses' not in st.session_state:
    st.session_state.text_responses = []
if 'image_responses' not in st.session_state:
    st.session_state.image_responses = []
if 'pdf_responses' not in st.session_state:
    st.session_state.pdf_responses = []
if 'user_feedback' not in st.session_state:
    st.session_state.user_feedback = []

# Constants and API Setup
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Tesseract OCR Path (adjust for your environment)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Utility Functions
def process_image(image_file):
    """Extract text from an uploaded image."""
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF."""
    try:
        text = ""
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text.strip()
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def get_ai_response(input_text, topic_type):
    """Fetch an AI-generated response based on user input and topic type."""
    try:
        system_message = f"""
        You are an AI-based study assistant. Provide hints and approaches to help users learn effectively without revealing exact answers.
        Ensure each response encourages critical thinking. Provide resources and tips relevant to the topic: {topic_type}.
        """
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": input_text},
                {"role": "user", "content": "Can you recommend resources (books, videos, quizzes) related to this topic?"}
            ],
            model="llama-3.1-70b-versatile",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return None

# Streamlit Configuration and Styling

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom right, #eef2f3, #d7e3fc);
    }
    .main-header {
        font-size: 2.5em;
        text-align: center;
        font-weight: bold;
        color: #2d3748;
    }
    .sub-header {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 20px;
        color: #4a5568;
    }
    .response-card {
        background-color: #fff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
    .hint-text {
        background-color: #f7fafc;
        padding: 10px;
        border-left: 3px solid #3182ce;
        margin-top: 10px;
        font-size: 0.95em;
        color: #2c5282;
    }
    .footer {
        text-align: center;
        font-size: 0.9em;
        margin-top: 20px;
        color: #718096;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("AI Smart Study Assistant")
topic_type = st.sidebar.radio("Select Topic Area:", ("General", "Machine Learning and Statistics", "AI", "Computer Networks"))

# Main Header
st.markdown("<h1 class='main-header'>AI Smart Study Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Personalized Study Guidance at Your Fingertips</h2>", unsafe_allow_html=True)


# Step 1: Basic Details
st.header("User Profile Setup")
name = st.text_input("Full Name")
age = st.number_input("Age (Optional)", min_value=0, step=1)

# Step 2: Academic Level
academic_level = st.selectbox("Academic Level", ["Undergraduate", "Graduate", "Postgraduate", "PhD", "Other"])

# Step 3: Field of Study
field_of_study = st.selectbox("Field of Study", ["Computer Science", "Engineering", "Medicine", "Business Administration", 
                                                 "Arts and Humanities", "Law", "Natural Sciences", "Other"])

# Step 4: Areas of Interest
interests = st.multiselect("Areas of Interest", ["Machine Learning & AI", "Statistics", "Programming & Development", 
                                                 "Computer Networks", "Research Methods", "Data Science", 
                                                 "Exam Preparation", "Other"])

# Step 5: Goals
goal = st.selectbox("Primary Goal", ["Improve academic performance", "Prepare for exams", 
                                     "Enhance understanding of specific topics", "Research assistance", 
                                     "Career preparation", "Other"])

# Step 6: Skill Levels
st.subheader("Skill Level (Optional)")
programming_level = st.slider("Programming Skill (1: Beginner → 10: Expert)", 1, 10, 5)
math_level = st.slider("Math/Statistics Skill (1 → 10)", 1, 10, 5)

# Step 7: Learning Style
learning_style = st.radio("Preferred Learning Style", ["Visual (videos, images)", 
                                                       "Text-based (articles, books)", 
                                                       "Hands-on (projects, coding exercises)", 
                                                       "Mixed"])

# Step 8: Feedback Frequency
feedback_frequency = st.radio("Feedback Frequency", ["Weekly progress reports", "Monthly updates", "No feedback needed"])

# Display profile summary
if st.button("Save Profile"):
    st.success("Profile Saved!")
    st.write(f"**Name:** {name}")
    st.write(f"**Age:** {age}")
    st.write(f"**Academic Level:** {academic_level}")
    st.write(f"**Field of Study:** {field_of_study}")
    st.write(f"**Areas of Interest:** {', '.join(interests)}")
    st.write(f"**Primary Goal:** {goal}")
    st.write(f"**Programming Skill Level:** {programming_level}")
    st.write(f"**Math Skill Level:** {math_level}")
    st.write(f"**Preferred Learning Style:** {learning_style}")
    st.write(f"**Feedback Frequency:** {feedback_frequency}")


# Tabs for Input
tabs = st.tabs(["📄 Text Input", "🖼️ Image Input", "📑 PDF Input"])

with tabs[0]:
    user_input = st.text_area("Enter your study question or topic:")
    if st.button("Get Hint"):
        if user_input:
            with st.spinner("Fetching hints..."):
                response = get_ai_response(user_input, topic_type)
                if response:
                    st.markdown("<div class='response-card'>", unsafe_allow_html=True)
                    st.markdown(f"<b>Hint:</b><div class='hint-text'>{response}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.session_state.text_responses.append((user_input, response))
        else:
            st.warning("Please enter a valid input.")

with tabs[1]:
    image_file = st.file_uploader("Upload an image (PNG, JPG):", type=["png", "jpg", "jpeg"])
    if st.button("Extract and Get Hint"):
        if image_file:
            with st.spinner("Processing image..."):
                extracted_text = process_image(image_file)
                if extracted_text:
                    response = get_ai_response(extracted_text, topic_type)
                    if response:
                        st.markdown("<div class='response-card'>", unsafe_allow_html=True)
                        st.markdown(f"<b>Extracted Text:</b> {extracted_text}", unsafe_allow_html=True)
                        st.markdown(f"<b>Hint:</b><div class='hint-text'>{response}</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.session_state.image_responses.append((extracted_text, response))
        else:
            st.warning("Please upload an image.")

with tabs[2]:
    pdf_file = st.file_uploader("Upload a PDF:", type=["pdf"])
    if st.button("Extract and Get Hint (PDF)"):
        if pdf_file:
            with st.spinner("Processing PDF..."):
                extracted_text = extract_text_from_pdf(pdf_file)
                if extracted_text:
                    response = get_ai_response(extracted_text, topic_type)
                    if response:
                        st.markdown("<div class='response-card'>", unsafe_allow_html=True)
                        st.markdown(f"<b>Extracted Text:</b> {extracted_text[:300]}...", unsafe_allow_html=True)
                        st.markdown(f"<b>Hint:</b><div class='hint-text'>{response}</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.session_state.pdf_responses.append((extracted_text, response))
        else:
            st.warning("Please upload a PDF.")

# Feedback Collection
st.sidebar.markdown("### Feedback")
feedback = st.sidebar.text_input("Provide feedback on the hints/resources:")
if st.sidebar.button("Submit Feedback"):
    if feedback:
        st.sidebar.success("Feedback submitted successfully!")
        st.session_state.user_feedback.append(feedback)

# Footer
st.markdown("<div class='footer'>© 2024 AI Study Assistant. Created by Abraham Pose Senteu</div>", unsafe_allow_html=True)
