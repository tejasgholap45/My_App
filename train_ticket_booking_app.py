import streamlit as st
from datetime import datetime
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="🚆 Train Ticket Booking", page_icon="🚆")

# ----- Dummy Train Data -----
TRAINS = {
    "Express 101": {"from": "Mumbai", "to": "Pune", "time": "08:00 AM", "price": 200},
    "Superfast 202": {"from": "Mumbai", "to": "Delhi", "time": "10:30 AM", "price": 1200},
    "Shatabdi 303": {"from": "Pune", "to": "Nagpur", "time": "06:45 AM", "price": 900},
    "Intercity 404": {"from": "Delhi", "to": "Jaipur", "time": "03:15 PM", "price": 500},
}

# ----- PDF Ticket Generator -----
def generate_ticket_pdf(name, train, passengers, date):
    train_info = TRAINS[train]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    pdf.cell(200, 10, "🚆 Train Ticket", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"Train: {train}", ln=True)
    pdf.cell(0, 10, f"From: {train_info['from']}  To: {train_info['to']}", ln=True)
    pdf.cell(0, 10, f"Departure: {train_info['time']}  Date: {date}", ln=True)
    pdf.cell(0, 10, f"Passengers: {passengers}", ln=True)

    total_price = train_info['price'] * passengers
    pdf.cell(0, 10, f"Total Fare: ₹{total_price}", ln=True)

    pdf.ln(10)
    pdf.cell(0, 10, "✅ Booking Confirmed. Have a safe journey!", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


# ----- Streamlit UI -----
st.title("🚆 Train Ticket Booking App")
st.write("Book your train tickets easily!")

with st.form("booking_form"):
    name = st.text_input("Passenger Name")
    train = st.selectbox("Select Train", list(TRAINS.keys()))
    passengers = st.number_input("Number of Passengers", min_value=1, step=1, value=1)
    date = st.date_input("Select Travel Date", datetime.today())

    submitted = st.form_submit_button("Book Ticket")

if submitted:
    if name.strip() == "":
        st.error("⚠️ Please enter passenger name")
    else:
        st.success("✅ Ticket booked successfully!")
        pdf_buffer = generate_ticket_pdf(name, train, passengers, date)

        st.download_button(
            label="🖨️ Download Ticket (PDF)",
            data=pdf_buffer,
            file_name="train_ticket.pdf",
            mime="application/pdf"
        )
