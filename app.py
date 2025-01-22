import streamlit as st
import pandas as pd
from main import extract_text_from_pdf, extract_multiple_details  # Import functions from main.py
import spacy
import sys

#import spacy
import sys
sys.path.append('models')  # Add the path to your models directory

nlp = spacy.load("en_core_web_sm")  # Now it loads from the local folder


# Streamlit Web App
st.title("PDF Data Extraction Web App")
st.write("Upload a PDF file containing structured data to extract details like Name, Phone, Address, and Role.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    st.info("Processing the uploaded PDF...")

    # Use the function imported from main.py
    extracted_text = extract_text_from_pdf(uploaded_file)
    if extracted_text:
        extracted_details_df = extract_multiple_details(extracted_text)

        st.subheader("Extracted Details")
        st.dataframe(extracted_details_df)

        csv = extracted_details_df.to_csv(index=False)
        st.download_button(
            label="Download Extracted Details as CSV",
            data=csv,
            file_name="extracted_details.csv",
            mime="text/csv",
        )
