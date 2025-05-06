import streamlit as st
import re
import random

# Common weak passwords to avoid
blacklist = ["password", "123456", "12345678", "password123", "qwerty", "abc123", "111111", "123123"]

def check_password_strength(password):
    feedback = []
    score = 0

    if password.lower() in blacklist:
        feedback.append("❌ Your password is too common and easily guessable.")
        return score, feedback

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    if len(password) >= 12:
        score += 1  # Bonus point for longer passwords

    return score, feedback

def generate_strong_password(length=12, use_upper=True, use_digits=True, use_specials=True):
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if use_upper else ""
    digits = "0123456789" if use_digits else ""
    specials = "!@#$%^&*" if use_specials else ""
    all_chars = lower + upper + digits + specials

    if not all_chars or length < 4:
        return "Invalid settings"

    # Ensure at least one character from each enabled set
    password = [random.choice(lower)]
    if use_upper:
        password.append(random.choice(upper))
    if use_digits:
        password.append(random.choice(digits))
    if use_specials:
        password.append(random.choice(specials))

    while len(password) < length:
        password.append(random.choice(all_chars))

    random.shuffle(password)
    return ''.join(password)

# Streamlit UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

st.title("🔐 Password Strength Meter")
st.subheader("Check how strong your password is!")

# Password visibility toggle
show_password = st.checkbox("Show password")
password = st.text_input("Enter your password", type="default" if show_password else "password")

if password:
    score, feedback = check_password_strength(password)

    st.divider()

    strength_levels = {
        0: ("❌ Very Weak", "red"),
        1: ("❌ Weak", "red"),
        2: ("⚠️ Fair", "orange"),
        3: ("⚠️ Moderate", "orange"),
        4: ("✅ Good", "green"),
        5: ("✅ Strong", "green"),
        6: ("✅ Excellent", "green"),
    }

    label, color = strength_levels.get(score, ("Unknown", "gray"))
    st.markdown(f"**Strength Score:** `{score}/6`")
    st.progress(score / 6)
    st.markdown(f"<span style='color:{color}; font-size: 1.2em;'>{label}</span>", unsafe_allow_html=True)

    if feedback:
        st.write("### Suggestions to improve:")
        for tip in feedback:
            st.write(tip)

# Password Generator Section
st.divider()
st.subheader("🔧 Need help creating a strong password?")

length = st.slider("Password Length", min_value=8, max_value=32, value=12)
use_upper = st.checkbox("Include Uppercase Letters", value=True)
use_digits = st.checkbox("Include Numbers", value=True)
use_specials = st.checkbox("Include Special Characters", value=True)

if st.button("Generate Strong Password"):
    new_password = generate_strong_password(length, use_upper, use_digits, use_specials)
    st.success(f"🔑 Suggested Password: `{new_password}`")
