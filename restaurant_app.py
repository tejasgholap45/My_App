import streamlit as st

# ----- USER CREDENTIALS -----
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

# ----- MAIN APP -----
def restaurant_app():
    st.sidebar.button("🚪 Logout", on_click=logout)

    # Initialize menu only once
    if 'menu' not in st.session_state:
        st.session_state.menu = {
            "Burger": 120,
            "Pizza": 250,
            "Pasta": 180,
            "Fries": 100,
            "Coke": 40
        }

    st.title("🍴 Welcome to Sai Restaurant")

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
                st.write("### 🧾 Bill")
                for item, qty in order.items():
                    price = st.session_state.menu[item] * qty
                    st.write(f"{item} x {qty} = ₹{price}")
                    total += price
                st.write(f"### ✅ Total: ₹{total}")
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
