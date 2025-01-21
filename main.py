import re
import spacy
import pandas as pd
import pdfplumber
import os
import spacy
import os

# Ensure the SpaCy model is available
if not os.path.exists(spacy.util.get_package_path("en_core_web_sm", allow_null=True)):
    from spacy.cli import download
    download("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    try:
        # Open the PDF file
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            # Iterate through all pages in the PDF
            for page in pdf.pages:
                text += page.extract_text()
        
        if text:
            print("text succesfully extracted")
        else:
            print("No text found in the PDF.")
        
        return text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_details(entry_text):
    """
    Extracts details (Name, Phone, Address, Role) from a single entry of text.
    """
    # Load the spaCy English model for NER (Named Entity Recognition)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(entry_text)

    # Extract Name (Using regex for better accuracy since NER might not work well here)
    name_pattern = re.compile(r"Name\s*[:\-]?\s*([^\n]+)")
    name_match = re.search(name_pattern, entry_text)
    name = name_match.group(1).strip() if name_match else None

    # Extract Phone Number
    phone_number_regex = r'\+?\d{1,2}[\s\-]?\(\d{1,5}\)[\s\-]?\d{1,5}[\s\-]?\d{1,5}(?![\s\-]?\d{5}\b)'
    phone_number = re.search(phone_number_regex, entry_text)
    phone = phone_number.group(0).strip() if phone_number else None

    # Extract Address (refined pattern)
    address_pattern = re.compile(
        r'Address\s*[:\-]?\s*(\d{1,5}[\w\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Lane|Boulevard|Drive|Blvd)[\w\s,]*)',
        re.IGNORECASE
    )
    address_match = re.search(address_pattern, entry_text)
    address = address_match.group(1).strip() if address_match else None

    # Extract Role
    role_pattern = re.compile(r'Role\s*[:\-]?\s*(.*)', re.IGNORECASE)
    role_match = re.search(role_pattern, entry_text)
    role = role_match.group(1).strip() if role_match else None

    # Return extracted details as a dictionary
    return {
        "Name": name,
        "Phone Number": phone,
        "Address": address,
        "Role": role,
    }

def extract_multiple_details(text):
    """
    Splits the input text into multiple entries and extracts details for each entry.
    """
    # Split the text by 'Name :' to handle multiple entries
    entries = text.split('Name : ')[1:]  # Ignore the first part before the first 'Name :'

    all_details = []
    for entry in entries:
        entry = 'Name : ' + entry  # Add 'Name :' back to the start of the entry
        details = extract_details(entry)
        all_details.append(details)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(all_details)
    return df

if __name__ == "__main__":
    # Replace with the path to your PDF file
    current_directory = os.getcwd()  # Get the current directory
    pdf_path = os.path.join(current_directory, "Multiple sample Data.pdf")
    
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
    else:
        # Extract text and details
        extracted_text = extract_text_from_pdf(pdf_path)
        if extracted_text:
            df = extract_multiple_details(extracted_text)
            print(df)

        
   
