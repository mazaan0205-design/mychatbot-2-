import streamlit as st
from groq import Groq
import time

# --- SETUP ---
st.set_page_config(page_title="Smile Crafters Assistant", page_icon="🦷")
st.title("🦷 Smile Crafters AI")

# --- API KEY (FIXED FOR STREAMLIT SECRETS) ---
# This line now correctly pulls the key from your Secrets box
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- THE BRAIN (FROM SHAWN'S TRAINING MANUAL) ---
SYSTEM_PROMPT = """
You are the Lead Assistant for Smile Crafters. 

STRICT FORMATTING RULES (FAILURE TO FOLLOW THESE WILL LOSE THE JOB):
1. You must answer in exactly ONE paragraph. No line breaks. No bullet points.
2. NEVER use quotation marks (") or apostrophes (').
3. NEVER mention you are an AI or a chatbot.
4. End every single response by asking to book a free 15-minute virtual consultation.

KNOWLEDGE BASE:
- Our veneers are handmade works of art from top-grade Swiss porcelain, lasting 15 to 20 years.
- We spend 10 to 15 hours on a precise 3D smile design phase for each patient.
- Patients get to wear temporary veneers as a test-drive before the final ones are bonded.
- We use the Advanced X Nav system for 100% precision in dental implants.
- INSURANCE: We accept most PPO plans. We DO NOT accept Medicaid, Medical, Medicare, State insurance, or HMO.
- PRICING: Financing starts as low as 299 dollars a month for 8 to 10 upper veneers.
- LOCATION: We are located in Los Angeles.
- If asked for phone or email, tell them those details are provided during the 15-minute consultation.
"""

# --- CHAT INTERFACE ---
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
            time.sleep(2) # 2-second delay for realism
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
            )
            response = completion.choices[0].message.content
            
            # EMERGENCY SAFETY FILTER: Removes any quotes or line breaks the AI accidentally adds
            final_txt = response.replace('"', '').replace("'", "").replace("\n", " ")
            
            st.write(final_txt)
            st.session_state.messages.append({"role": "assistant", "content": final_txt})
