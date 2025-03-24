import re
import secrets
import string
import streamlit as st
from datetime import datetime

#page styling
st.set_page_config(page_title= "PassCheck: Password Validator", page_icon="🛡️", layout="centered")


st.title("🔑 PassCheck: Password Validator")
st.markdown("Instantly assess how secure your password is.")

# Sidebar Title
st.sidebar.title("🔍 Explore")

if "password_history" not in st.session_state:
    st.session_state.password_history = []

# Create tab-like buttons
tabs = st.sidebar.tabs(["🔒 Security Tips", "🎉 Fun Fact", "📜 History"])

# Security Facts Section
with tabs[0]:  # Security Tips Tab
    st.subheader("🔒 Security Tips")
    with st.expander("🛡️ Password Length"):
        st.markdown("- Use **at least 8 characters** for a strong password.")

    with st.expander("🔠 Mix of Letters"):
        st.markdown("- Include **both uppercase and lowercase letters**.")

    with st.expander("🔢 Include Numbers"):
        st.markdown("- Add **numbers (0-9)** to enhance security.")

    with st.expander("🔣 Special Characters"):
        st.markdown("- Use **special characters (!@#$%^&* etc.)**.")

    with st.expander("🚫 Avoid Common Words"):
        st.markdown("- Avoid using **common words or personal information**.")

    with st.expander("🔐 Use a Password Manager"):
        st.markdown("- Consider using a **password manager** for secure storage.")

    with st.expander("🔄 Change Passwords Regularly"):
        st.markdown("- Change your password **periodically** to stay secure.")

# Fun Fact Section
with tabs[1]:  
    st.subheader("🎉 Fun Fact")
    st.markdown("Did you know? The longest password ever used was **585 characters** long!")

# History Section
with tabs[2]:  
    st.subheader("📜 History of Passwords")
    # Display password history
    if st.session_state.password_history:
        for entry in reversed(st.session_state.password_history):  # Show newest first
            password, strength, timestamp = entry
           # Create a styled box for each password history entry
            with st.container():
                st.markdown(
                    f"""
                    <div style="border: 2px solid #4CAF50; padding: 8px; margin: 2px 0; border-radius: 10px; background-color: #f9f9f9;">
                        <p><strong>🔑 Password:</strong> {password}</p>
                        <p><strong>📊 Strength:</strong> {strength}</p>
                        <p><strong>⏳ Checked on:</strong> {timestamp}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.password_history = []
            st.rerun()
    else:
        st.info("No passwords checked yet.")



def check_password(password):
    score = 0
    feedback = []
    length = len(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*()_+{}|:\"<>?\[\];',./`~\\]", password))


    if length >= 8:
        score +=1
    else:
        feedback.append("password should be **8 characters long**")

    if has_upper and has_lower:
        score +=1
    else:
        feedback.append("password should contain **both uppercase [A-Z] and lowercase [a-z] letters**")

    if has_digit:
        score +=1
    else:
        feedback.append("password should contain **atleast one number (0-9)**")

    if has_special:
        score +=1
    else:
        feedback.append("password should contain **atleast one special character)**")

#display results
    if score == 4:
        strength = "✅ Strong"
        st.success("Great job! Your password is **strong** and well-protected. 🔒")
    elif score == 3:
        strength = "⚠️ Moderate"
        st.warning("Your password is **moderate**. Consider adding more complexity for better security. 🛡️")
    else:
        strength = "❌ Weak"
        st.error("Your password is **weak**. Try making it longer and adding a mix of characters. 🚨")

# Save to history with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.password_history.append((password, strength, timestamp))

    #feedback display
    if feedback:
        with st.expander("🔧 Suggestions to Strengthen Your Password"):
            for item in feedback:
                st.caption(f"⚡ {item}")
    
    # Display results
    st.markdown("### **Password Analysis**")

    # Length Check
    if length >= 8:
        st.markdown(f"✅ **Length:** Secure ({length} characters) - Meets recommended length!")
    else:
        st.markdown(f"❌ **Length:** Too short ({length} characters) - Aim for at least **8 characters** for better security.")

    # Character Type Check
    st.markdown("### **Character Types:**")
    st.markdown(f"{'✅' if has_upper else '❌'} **Uppercase letters**")
    st.markdown(f"{'✅' if has_lower else '❌'} **Lowercase letters**")
    st.markdown(f"{'✅' if has_digit else '❌'} **Numbers**")
    st.markdown(f"{'✅' if has_special else '❌'} **Special characters**")

# Function to generate a strong password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+{}|:\"<>?\[\];',./`~\\"
    return ''.join(secrets.choice(characters) for _ in range(length))

password = st.text_input("Input a password to check its strength:", type="password", help="Create a strong password at least 8 characters long with a mix of letters, numbers, and symbols.")
st.caption("🔒 All analysis is done locally in your browser, keeping your password secure.")

if st.button("Check Strength"):
    if password:
        check_password(password)
    else:
        st.warning("please enter your password first")

# Password Generator Feature
st.markdown("---")
st.subheader("🔹 Need a Strong Password? Generate One Instantly!")

if st.button("⚡ Generate Strong Password"):
    new_password = generate_password()
    st.markdown("Here is a strong password:")
    st.code(new_password, language="plaintext", line_numbers=False)
    # Caption aligned to the right
    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; font-size: 0.9em; font-style: italic; color: gray;">
            Copy and use this password securely!
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.markdown("Created with ❤️ by Urooj Sadiq - [Connect on LinkedIn](https://www.linkedin.com/in/urooj-sadiq-a91031212/)")

