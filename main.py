
import streamlit as st
import time
import random
from groq import Groq

# 1. SETUP & THEME
st.set_page_config(page_title="Smile Crafters Concierge", layout="centered")
st.title("🦷 Smile Crafters AI")

# 2. DATA & IDENTITY (From the Dental Manual)
# Ensure you replace this with your actual key or set it in Streamlit Secrets
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE") 

SYSTEM_PROMPT = (
    "You are the elite, warm concierge for Smile Crafters. "
    "CRITICAL RULES: 1. Always answer in exactly ONE PARAGRAPH. 2. NEVER use line breaks. "
    "3. NEVER use quotation marks. 4. Never reveal you are an AI. 5. Keep it punchy and short. "
    "KNOWLEDGE: We use Swiss-made porcelain and Swiss-made implants (X Nav system). "
    "No composite veneers. We offer no-prep, minimal prep, and regular prep. "
    "The smile design phase takes 10 to 15 hours with 3D rendering. "
    "Financing: $299/mo for 8-10 veneers or $399/mo for 16-20 veneers. "
    "Insurance: We accept most PPO. No Medicaid, Medicare, HMO, or State insurance. "
    "Parking entrance is on the right-hand side. The doctor takes limited patients per month. "
    "If veneers are mentioned, recommend the Current Promotion button. "
    "Always end by offering a free 15-minute virtual consultation or a faster in-person visit."
)

# 3. DYNAMIC DELAY (Shawn's Rule: 5-10 seconds based on length)
def apply_human_delay(text):
    word_count = len(text.split())
    # Short answers (~20 words) get ~5s, Long answers (~60 words) get ~10s
    delay = 5 + (min(word_count, 60) / 60) * 5 
    time.sleep(delay + random.uniform(-0.5, 0.5))

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

        # B. THE SHIELD (Force formatting requirements)
        clean_response = response.replace('"', '').replace("'", "")
        clean_response = " ".join(clean_response.split()) # Removes any hidden line breaks

        # C. THE DELAY (Wait before showing the message)
        with st.spinner("Typing..."):
            apply_human_delay(clean_response)

        # D. DISPLAY
        st.markdown(clean_response)
        st.session_state.messages.append({"role": "assistant", "content": clean_response})
