import streamlit as st
from datetime import date

st.title("VA Form 21-0781 PTSD Statement Generator")

st.markdown("""
This app helps you draft your VA Form 21-0781 (Statement in Support of Claim for PTSD) by answering a few simple questions.
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

# Generate formatted PTSD narrative
if st.button("Generate 21-0781 Statement"):
    statement = f"""
VA Form 21-0781 - Statement in Support of Claim for PTSD

Veteran Name: {veteran_name}
SSN (Last 4): {ssn_last4}
Date of Event: {date_of_event.strftime('%B %d, %Y')}
Location of Event: {location}
Unit Assigned: {unit}
Others Involved: {involved_names}

Description of the Event:
{stressor_description}

How I Reacted:
{reaction}

Ongoing Effects:
{current_effects}

Did I Report It?: {reported}
"""

    st.download_button(
        label="Download Your Statement",
        data=statement,
        file_name="VA_Form_21-0781_Statement.txt",
        mime="text/plain"
    )

    st.text_area("Your Generated Statement:", statement, height=300) 
