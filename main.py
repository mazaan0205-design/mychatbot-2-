import streamlit as st
import time
import random
from groq import Groq

# 1. PAGE SETUP
st.set_page_config(page_title="Smile Crafters Concierge", layout="centered")
st.title("🦷 Smile Crafters AI")

# 2. SECURE API KEY LOAD
# This fix solves the "AuthenticationError" in your screenshot
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Please add your 'GROQ_API_KEY' to Streamlit Secrets!")
    st.stop()

# 3. CONSOLIDATED SYSTEM PROMPT (All rules merged)
SYSTEM_PROMPT = (
    "You are the elite, warm concierge for Smile Crafters. "
    "CRITICAL RULES: 1. Always answer in exactly ONE PARAGRAPH. 2. NEVER use line breaks. "
    "3. NEVER use quotation marks. 4. Never reveal you are an AI. 5. Be concise and punchy. "
    "KNOWLEDGE: We use Swiss-made porcelain and Swiss-made implants (X Nav system). "
    "The smile design phase takes 10 to 15 hours. Financing: $299/mo (8-10 veneers) or $399/mo (16-20). "
    "Insurance: PPO only. No Medicaid, Medicare, HMO, or State insurance. "
    "Parking entrance is on the right-hand side. The doctor takes limited patients. "
    "If veneers are mentioned, recommend the Current Promotion button. "
    "End by offering a free 15-minute virtual consultation or a faster in-person visit."
)

# 4. CHAT LOGIC
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # A. Call Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=0.6
        )
        response = completion.choices[0].message.content

        # B. SHIELD (Force formatting)
        clean_response = response.replace('"', '').replace("'", "")
        clean_response = " ".join(clean_response.split())

        # C. PROPORTIONAL DELAY (Shawn's 5-10 second rule)
        with st.spinner("Typing..."):
            word_count = len(clean_response.split())
            # Proportional wait: short answers = 5s, long = 10s
            wait_time = 5 + (min(word_count, 60) / 60) * 5 
            time.sleep(wait_time + random.uniform(-0.5, 0.5))

        # D. DISPLAY
        st.markdown(clean_response)
        st.session_state.messages.append({"role": "assistant", "content": clean_response})


