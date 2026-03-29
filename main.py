import streamlit as st
from groq import Groq
import time

# --- SETUP ---
st.set_page_config(page_title="Smile Crafters Assistant", page_icon="🦷")
st.title("🦷 Smile Crafters AI")

# --- API KEY ---
# Replace the text below with your actual Groq API Key
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

# --- THE BRAIN (From your 2 clear photos) ---
SYSTEM_PROMPT = """
You are the Lead Assistant for Smile Crafters. 
STRICT FORMATTING RULES:
1. You must answer in exactly ONE paragraph.
2. Never use quotation marks (" ").
3. Never mention you are an AI.
4. Do not use line breaks.
5. End every message by asking to book a free 15-minute virtual consultation.

KNOWLEDGE BASE:
Our porcelain veneers are handmade works of art from top-grade Swiss porcelain, lasting 15 to 20 years. 
We spend 10 to 15 hours on a precise 3D smile design phase before starting. 
Patients wear temporary veneers to test-drive their smile. 
We use the Advanced X Nav system for precise implants. 
We accept PPO insurance but NOT Medicaid, Medical, Medicare, or HMO. 
Financing starts at 299 dollars a month for 8 to 10 upper veneers. 
We are located in Los Angeles.
"""

# --- THE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask about your new smile..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # SHAWN'S DELAY REQUIREMENT
        with st.spinner("Typing..."):
            time.sleep(2) 
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
            )
            response = completion.choices[0].message.content
            # Safety filter to remove any quotes the AI might use
            final_txt = response.replace('"', '').replace("'", "")
            st.write(final_txt)
            st.session_state.messages.append({"role": "assistant", "content": final_txt})
