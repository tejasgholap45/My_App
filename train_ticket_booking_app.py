import streamlit as st
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

# ----- PDF Generator -----
def generate_ticket_pdf(name, train, passengers, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 14)

    # Ticket title
    pdf.cell(200, 10, txt="Train Ticket", ln=True, align="C")
    pdf.ln(10)

    # Ticket details
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Train: {train}", ln=True)
    pdf.cell(200, 10, txt=f"Passengers: {passengers}", ln=True)
    pdf.cell(200, 10, txt=f"Date of Journey: {date}", ln=True)

    # Timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Issued On: {now}", ln=True)

    # Get PDF as bytes for Streamlit download
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    buffer = BytesIO(pdf_bytes)
    return buffer

# ----- Streamlit UI -----
st.title("Train Ticket Booking App")

name = st.text_input("Enter Passenger Name")
train = st.selectbox("Select Train", ["Express 101", "Superfast 202", "Rajdhani 303"])
passengers = st.number_input("Number of Passengers", min_value=1, step=1)
date = st.date_input("Select Journey Date")

if st.button("Book Ticket"):
    if name.strip() == "":
        st.error("Please enter passenger name")
    else:
        pdf_bytes = generate_ticket_pdf(name, train, passengers, date)
        st.success("Ticket booked successfully!")
        st.download_button(
            label="Download Ticket (PDF)",
            data=pdf_bytes,
            file_name="train_ticket.pdf",
            mime="application/pdf"
        )
