import streamlit as st
import fitz  # PyMuPDF for PDF processing
import os
import openai

# Function to extract text from all PDFs in a specified folder
def load_and_extract_texts_from_folder(folder_path):
    texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            texts[filename] = text
    return texts

# Initialize Streamlit app
st.title("Document Query Tool with Advanced Query Handling")

# Load extracted texts from PDFs located in 'data1' folder
extracted_texts = load_and_extract_texts_from_folder("data1")

# Input for complex queries
query = st.text_input("Enter your complex query:")

if query and extracted_texts:
    # Combine texts for processing (consider optimizing based on your needs)
    combined_text = " ".join(extracted_texts.values())[:4000]  # Limit to 4000 characters for API constraints
    
    # OpenAI API setup
    openai.api_key = st.secrets["openai_key"]
    
    try:
        # Using OpenAI's "davinci" engine for Q&A based on the combined text
        response = openai.Completion.create(
          engine="davinci",
          prompt=f"Answer the following question based on the document: {query}",
          temperature=0.5,
          max_tokens=100,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0,
          stop=["\n"],
          documents=[combined_text]  # Using the combined text as context
        )
        
        # Displaying the response from OpenAI's model
        st.text_area("Result", value=response.choices[0].text.strip(), height=300, help="Response from OpenAI's model.")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
