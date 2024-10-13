import streamlit as st
from transformers import pipeline
import PyPDF2
import io
import fitz 
import requests
from io import BytesIO
from PIL import Image

# Initialize the question-answering pipeline
question_answerer = pipeline("question-answering")
summarizer = pipeline("summarization")


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with io.BytesIO(pdf_file.read()) as pdf_file_stream:
            reader = PyPDF2.PdfReader(pdf_file_stream)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text
# Function to extract text from a PDF file using PyMuPDF
def pdf_to_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text
# Function to extract text from TXT files
def extract_text_from_txt(txt_file):
    try:
        return txt_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading TXT file: {e}")
        return ""
# Set the page configuration (optional)

st.set_page_config(page_title="DiscoverNote", layout="wide")

# CSS Styling

backgroundImg = '''
<style>
.stApp {
    background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
    url("https://community.nasscom.in/sites/default/files/media/images/NLP-image.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
'''
page_bg_img = '''
<style>

.navbar {
    overflow: hidden;
    background-color: #333;
    position: fixed;
    top: 0;
    width: 100%;
    display: flex;
    justify-content: space-around;
    padding: 10px;
    z-index: 100;
}

.navbar h3 {
    color: white;
    margin: 0;
    padding: 0 15px;
}

.center-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
    color: white;
    text-align: center;
    flex-direction: column;
}
</style>
'''

# Inject CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Display Navbar
st.markdown('<div class="navbar"><h3>DiscoverNote</h3></div>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("JiTECH")
page = st.sidebar.radio("Go to", ["Home", "About", "Services", "Contact"])

# Content Rendering
if page == "Home":
    st.markdown(backgroundImg, unsafe_allow_html=True)
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.header("Welcome to our homepage!")
    st.write("DiscoverNote helps students and professionals manage documents efficiently.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "About":
    st.header("About JiTECH")
    st.write("""
        Welcome to **JiTECH**, an innovative platform designed to make life easier for students 
        and professionals with heavy workloads. Our mission is to simplify note-taking, studying, 
        and document management by providing efficient tools for **summarizing PDFs, extracting key information,** 
        and allowing users to **ask questions about their documents** with ease.
        
        ### Our Vision
        At JiTECH, we aim to:
        - **Reduce stress** by saving time spent manually going through lengthy documents.
        - **Empower students and professionals** to focus on what matters most.
        - Deliver **AI-powered solutions** that bring clarity and simplicity to complex materials.
        
        ### Why Use JiTECH?
        - **Automated PDF Summarization:** Upload your PDFs and get concise summaries instantly.
        - **Intelligent Q&A System:** Ask questions about the content of your documents.
        - **User-Friendly Interface:** Designed for ease of use, even with a busy schedule.

        JiTECH is your personal study assistant, transforming overwhelming tasks into manageable ones. 
        Whether you're preparing for exams, handling research, or working with complex notes, JiTECH is here to help.
    """)


elif page == "Services":
    st.header("Our Services")
    st.write("Select a service below to get started:")

    service = st.sidebar.selectbox(
        "Choose a Service", 
        ["Summarize PDFs", "Ask Questions about Notes", "Manage and Organize Notes"]
    )

    if service == "Summarize PDFs":
        st.subheader("Summarize Documents")
    st.write("Upload your documents (PDF, TXT, or others) to receive concise summaries.")
    
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "docx", "md"])
    
    if uploaded_file:
        st.success("File uploaded successfully! Extracting and summarizing...")

        # Extract text based on file type
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file) or pdf_to_text(uploaded_file)
        elif file_type == "text/plain":
            text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a PDF or TXT file.")
            text = ""

        # Proceed with summarization if text is extracted
        if text:
            st.subheader("Extracted Text (Optional Preview)")
            st.write(text[:1000] + "...")  # Display the first 1000 characters

            # Summarize the extracted text
            if len(text.split()) > 500:
                text = " ".join(text.split()[:500])  # Limit to first 500 words

            summary = summarizer(text, max_length=130, min_length=30, do_sample=False)

            # Display the summary
            st.subheader("Summary")
            st.write(summary[0]['summary_text'])

    elif service == "Ask Questions about Notes":
        st.subheader("Ask Questions about Notes")
        uploaded_file = st.file_uploader("Upload your notes (PDF or text)", type=["pdf", "txt"])
        question = st.text_input("What would you like to ask?")

        if uploaded_file and question:
            if uploaded_file.type == "text/plain":
                # Read and decode the content of the TXT file
                context = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":
                # Extract text from the PDF file
                context = pdf_to_text(uploaded_file)

            # Perform question answering
            result = question_answerer(question=question, context=context)
            st.write("Answer:", result['answer'])


    elif service == "Manage and Organize Notes":
        st.subheader("Manage and Organize Notes")
        st.write("""
            Store, categorize, and organize your notes efficiently. Track summaries, manage study material, 
            and access notes easily in one place.
        """)

elif page == "Contact":
    

# Social media links and icons
    social_media = {
    "GitHub": {
        "url": "https://github.com/JamesMungai254/",
        "icon": "https://cdn-icons-png.flaticon.com/512/25/25231.png"
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/james-mungai-b6462a2a3",
        "icon": "https://cdn-icons-png.flaticon.com/512/174/174857.png"
    },
    "Email": {
        "url": "mailto:jamesmungai6303@gmail.com",
        "icon": "https://cdn-icons-png.flaticon.com/512/732/732200.png"
    },
    "Twitter": {
        "url": "https://x.com/JamesMunga254",
        "icon": "https://cdn-icons-png.flaticon.com/512/733/733579.png"
    }
}

# Contact Page Layout
    st.title("Contact Us")
    st.write("Feel free to reach out to us through the following platforms:")

# Display social media icons with links
    cols = st.columns(len(social_media))  # Create dynamic columns based on the number of platforms

    for index, (platform, info) in enumerate(social_media.items()):
    # Load the icon from URL
        response = requests.get(info["icon"])
        icon = Image.open(BytesIO(response.content))

    # Display the icon with a clickable link
        with cols[index]:
           st.markdown(
            f"""
            <a href="{info['url']}" target="_blank">
                <img src="{info['icon']}" width="50" height="50" style="margin:10px"/>
            </a>
            <br>{platform}
            """,
            unsafe_allow_html=True
        )
