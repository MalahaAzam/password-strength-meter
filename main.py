import streamlit as st
import re
import random

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
        score += 1  # Bonus point for length

    return score, feedback

def generate_strong_password(length=12):
    if length < 8:
        length = 12

    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    specials = "!@#$%^&*"
    all_chars = lower + upper + digits + specials

    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(specials)
    ]

    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

# Streamlit App UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

st.title("🔐 Password Strength Meter")
st.subheader("Check how strong your password is!")

password = st.text_input("Enter your password", type="password")

if password:
    score, feedback = check_password_strength(password)

    st.divider()

    if score >= 5:
        st.success("✅ Strong Password! Great job!")
    elif 3 <= score < 5:
        st.warning("⚠️ Moderate Password - Consider improving it.")
    else:
        st.error("❌ Weak Password - You should definitely improve it.")

    if feedback:
        st.write("### Suggestions to improve:")
        for tip in feedback:
            st.write(tip)

# Strong Password Generator
st.divider()
st.subheader("Need help creating a strong password?")

if st.button("Generate Strong Password"):
    new_password = generate_strong_password()
    st.success(f"🔑 Suggested Password: `{new_password}`")
