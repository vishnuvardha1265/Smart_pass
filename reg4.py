import streamlit as st
import re
import random
import string

st.set_page_config(page_title="🔐 Smart Password Checker", layout="centered")
st.title("🔐 Smart Password Checker")

st.markdown("""
**Password must contain:**
- At least 8 characters  
- At least one uppercase letter  
- At least one lowercase letter  
- At least one number  
- At least one special character (`!@#$%^&*`)  
""")

# --- Password checker ---
def check_password_strength(pwd):
    if len(pwd) < 8:
        return False, "❌ Too short (min 8 characters)"
    if not re.search(r"[A-Z]", pwd):
        return False, "❌ Missing uppercase letter"
    if not re.search(r"[a-z]", pwd):
        return False, "❌ Missing lowercase letter"
    if not re.search(r"\d", pwd):
        return False, "❌ Missing number"
    if not re.search(r"[!@#$%^&*]", pwd):
        return False, "❌ Missing special character (!@#$%^&*)"
    return True, "✅ Strong password"

# --- Password generator ---
def generate_strong_password(length=12):
    chars = (
        random.choice(string.ascii_uppercase) +
        random.choice(string.ascii_lowercase) +
        random.choice(string.digits) +
        random.choice("!@#$%^&*")
    )
    rest = ''.join(random.choices(
        string.ascii_letters + string.digits + "!@#$%^&*", k=length - 4))
    full_password = list(chars + rest)
    random.shuffle(full_password)
    return ''.join(full_password)

# --- Session state ---
if "show_generate" not in st.session_state:
    st.session_state.show_generate = False
if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""

# --- Input field ---
password = st.text_input("🔑 Enter your password:", type="password")

# --- Check password ---
if st.button("✅ Enter"):
    st.session_state.generated_password = ""  # CLEAR previously generated password

    if not password:
        st.warning("⚠️ Please enter a password first.")
        st.session_state.show_generate = False
    else:
        is_strong, feedback = check_password_strength(password)
        st.markdown(f"### Result: {feedback}")

        if is_strong:
            st.success("✅ Great! Your password is strong.")
            st.session_state.show_generate = False
        else:
            st.warning("Your password is weak. Would you like to generate a strong one?")
            st.session_state.show_generate = True

# --- Generate section ---
if st.session_state.show_generate:
    if st.button("🔐 Generate Strong Password"):
        st.session_state.generated_password = generate_strong_password()

    if st.session_state.generated_password:
        st.success(f"✅ Generated Password: `{st.session_state.generated_password}`")
        st.markdown("⚠️ Copy and save it securely.")
