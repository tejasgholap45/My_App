import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

# ----- LOGIN INFO -----
USERNAME = "admin"
PASSWORD = "1234"

# ----- LOGIN STATE -----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----- LOGIN PAGE -----
def login_page():
    st.title("🔐 Login to Sai Restaurant ")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

# ----- LOGOUT -----
def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()

# ----- MAIN RESTAURANT APP -----
def restaurant_app():
    st.sidebar.button("🚪 Logout", on_click=logout)

    if 'menu' not in st.session_state:
        st.session_state.menu = {
            "Burger": 120,
            "Pizza": 250,
            "aloo wada": 180,
            "Panir masala": 100,
            "Shev Bhaji": 40
        }

    st.title("🍴 Sai Restaurant ")

    tab1, tab2 = st.tabs(["🧑‍🍳 Customer", "🔐 Admin Panel"])

    # --- CUSTOMER SECTION ---
    with tab1:
        st.header("📋 Menu")
        for item, price in st.session_state.menu.items():
            st.write(f"**{item}** - ₹{price}")

        st.subheader("🛒 Place Your Order")

        order = {}
        for item in st.session_state.menu:
            qty = st.number_input(f"{item} (Qty)", min_value=0, max_value=10, step=1, key=item)
            if qty > 0:
                order[item] = qty

        if st.button("Generate Bill"):
            if order:
                total = 0
                bill_text = "🧾 BILL Thank You...visit Again\n\n"
                for item, qty in order.items():
                    price = st.session_state.menu[item] * qty
                    bill_text += f"{item} x {qty} = ₹{price}\n"
                    total += price
                bill_text += f"\nTOTAL = ₹{total}"

                st.text(bill_text)

                # ---- PDF Generation ----
                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=A4)
                text = c.beginText(50, 800)
                text.setFont("Helvetica", 12)

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                text.textLine(f"🧾 Python Restaurant Bill")
                text.textLine(f"Date/Time: {now}")
                text.textLine("------------------------------")
                for line in bill_text.split('\n'):
                    text.textLine(line)
                c.drawText(text)
                c.save()
                buffer.seek(0)

                st.download_button(
                    label="🖨️ Download & Print Bill (PDF)",
                    data=buffer,
                    file_name="restaurant_bill.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("Please select at least one item.")

    # --- ADMIN SECTION ---
    with tab2:
        st.header("🔧 Manage Menu (Admin Only)")

        st.subheader("➕ Add Item")
        new_item = st.text_input("Item Name").title()
        new_price = st.number_input("Item Price", min_value=1, step=1)

        if st.button("Add Item"):
            if new_item and new_item not in st.session_state.menu:
                st.session_state.menu[new_item] = new_price
                st.success(f"{new_item} added to menu!")
            else:
                st.error("Item already exists or name is empty!")

        st.subheader("❌ Remove Item")
        item_to_remove = st.selectbox("Select Item to Remove", list(st.session_state.menu.keys()))
        if st.button("Remove Item"):
            del st.session_state.menu[item_to_remove]
            st.warning(f"{item_to_remove} removed from menu.")

# ----- RUN APP -----
if st.session_state.logged_in:
    restaurant_app()
else:
    login_page()
