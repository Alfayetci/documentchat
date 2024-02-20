#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import fitz  # PyMuPDF
import os
import openai  # Import OpenAI library

# Setup OpenAI API key
openai.api_key = st.secrets["openai_key"]

# Define the path to the folder containing PDFs
PDF_FOLDER_PATH = "data1"

# Function to extract text from a PDF document
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Load and extract text from all PDFs in the specified folder
def load_and_extract_texts_from_folder(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(file_path)
            texts.append(text)
    return texts

# Main interface
st.title("Document Query Tool with OpenAI Integration")

# Assuming PDFs are preloaded, we extract texts from them
extracted_texts = load_and_extract_texts_from_folder(PDF_FOLDER_PATH)

# Simple function to simulate searching texts for a query
def simple_search(query, texts):
    # Very basic search: checks if query is in text
    return [text for text in texts if query.lower() in text.lower()]

# User inputs a query
query = st.text_input("Enter your question or keyword:")

if query:
    # Perform search
    search_results = simple_search(query, extracted_texts)
    if search_results:
        for result in search_results:
            # Displaying a portion of the results for readability
            st.text_area("Result", value=result[:1000], height=300, help="Showing a portion of the found text.")
    else:
        st.write("No results found.")

