import os
os.chdir("D:/python")

import streamlit as st
import pandas as pd
import io

# Title of the app
st.title("Student Presence Control")

# Predefined list of valid student emails
valid_emails = [
    "student1@example.com",
    "student2@example.com",
    "student3@example.com",
    "student4@example.com",
    "student5@example.com"
]

# Create a session state to store emails
if 'emails' not in st.session_state:
    st.session_state.emails = []

# Email input
email = st.text_input("Enter your email address:", "")

# Check if the email is valid (email should be in the predefined list)
def is_valid_email(email):
    return email in valid_emails

# Button to confirm presence
if st.button("OK"):
    if is_valid_email(email):
        # Add email to session state if it's valid and not already recorded
        if email not in st.session_state.emails:
            st.session_state.emails.append(email)
            st.success(f"Presence recorded for: {email}")
        else:
            st.warning(f"You have already recorded your presence, {email}.")
    else:
        st.error("Email not recognized. Please enter a valid email.")

# Display the list of recorded emails
st.write("---")
st.subheader("Recorded Present Students:")
if st.session_state.emails:
    for recorded_email in st.session_state.emails:
        st.write(recorded_email)
else:
    st.write("No students have marked their presence yet.")

# Export the presence list to Excel
if st.button("Download Presence List"):
    # Create a DataFrame from the list of emails
    df = pd.DataFrame(st.session_state.emails, columns=["Email"])

    # Create a BytesIO buffer to hold the Excel file
    output = io.BytesIO()

    # Save the DataFrame to the BytesIO buffer
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Presence List')

    # Set buffer position to the beginning
    output.seek(0)

    # Provide the download button with the buffer content
    st.download_button(
        label="Download Excel File",
        data=output,
        file_name="presence_list.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Footer of the app
st.write("---")
st.write("Thank you for participating!")