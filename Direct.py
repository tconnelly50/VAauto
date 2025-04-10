import streamlit as st
from datetime import date
from pdfrw import PdfReader, PdfWriter, PageMerge
from pdfrw import PdfDict, PdfName, PdfObject
import io

PDF_TEMPLATE_PATH = "VBA-21-0781-ARE.pdf"  # Make sure this file is in your project folder

st.title("VA Form 21-0781 PTSD Statement Generator")

st.markdown("""
This app helps you fill out VA Form 21-0781 (Statement in Support of Claim for PTSD). After you fill in the information below, it will generate a filled-in form you can download and submit.
""")

# Collect user input
veteran_name = st.text_input("Your Full Name")
ssn_last4 = st.text_input("Last 4 digits of your SSN")
date_of_event = st.date_input("Date of Stressful Event")
location = st.text_input("Location of Event")
unit = st.text_input("Unit Assigned During Event")
stressor_description = st.text_area("Describe the Traumatic Event")
involved_names = st.text_input("Who else was involved (names, ranks, witnesses)?")
reaction = st.text_area("How did you feel/react at the time?")
current_effects = st.text_area("How has the event affected you since?")
reported = st.radio("Did you report the event at the time?", ("Yes", "No"))

# Mapping of fields from form — update these based on actual PDF field names
form_fields = {
    '1. FULL NAME OF VETERAN': veteran_name,
    '2. SOCIAL SECURITY NUMBER': ssn_last4,
    '7A. DATE OF EVENT': date_of_event.strftime('%m/%d/%Y'),
    '7B. LOCATION': location,
    '7C. UNIT ASSIGNED': unit,
    '7D. DESCRIPTION OF INCIDENT': stressor_description,
    '7E. NAMES OF OTHERS INVOLVED': involved_names,
    '8. HOW DID YOU REACT?': reaction,
    '9. ONGOING EFFECTS': current_effects,
    '10. WAS IT REPORTED?': reported
}

# Fill and export the PDF
def fill_pdf(fields):
    template_pdf = PdfReader(PDF_TEMPLATE_PATH)
    for page in template_pdf.pages:
        annotations = page.get('/Annots')
        if annotations:
            for annotation in annotations:
                if annotation['/Subtype'] == '/Widget' and annotation.get('/T'):
                    key = annotation['/T'][1:-1]  # Clean the key
                    if key in fields:
                        annotation.update(
                            PdfDict(V='{}'.format(fields[key]), Ff=1)
                        )
    output_stream = io.BytesIO()
    PdfWriter().write(output_stream, template_pdf)
    return output_stream

if st.button("Generate Filled Form"):
    if not all([veteran_name, ssn_last4, stressor_description, reaction, current_effects]):
        st.warning("Please fill in all required fields.")
    else:
        pdf_bytes = fill_pdf(form_fields)
        st.download_button(
            label="Download Completed VA Form 21-0781",
            data=pdf_bytes,
            file_name="VA_Form_21-0781_Filled.pdf",
            mime="application/pdf"
        )
