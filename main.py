import streamlit as st
import time
import random
from groq import Groq

# 1. PAGE SETUP (Professional Appearance)
st.set_page_config(page_title="Smile Crafters Concierge", layout="centered")

# Custom CSS to make the UI look like a premium dental office
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("🦷 Smile Crafters Concierge")
st.caption("Elite General & Cosmetic Dentistry Specialist")

# 2. INITIALIZE GROQ & DATA
# Replace with your actual Groq Key
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")
MODEL = "llama-3.3-70b-versatile"

# The "Shawn-Specific" System Prompt (Baked with every rule discussed)
SYSTEM_PROMPT = (
    "You are the elite, warm concierge for Smile Crafters led by an honors graduate doctor from a prestigious university. "
    "CRITICAL CONSTRAINTS: 1. Always answer in exactly ONE PARAGRAPH. 2. NEVER use line breaks or bullet points. "
    "3. NEVER use quotation marks of any kind. 4. Never mention you are an AI. 5. Stay professional, warm, and concise. "
    "BUSINESS DATA: We offer Swiss-made porcelain veneers and implants (using the X Nav system). No composite veneers. "
    "Veneer options: no-prep, minimal prep, regular prep. The smile design phase takes 10 to 15 hours with 3D rendering. "
    "Financing: $299/mo for 8-10 veneers; $399+/mo for 16-20. We accept most PPO but NO Medicaid, Medicare, Medical, or HMO. "
    "Most dental insurance caps at $1500/year. Porcelain veneers last 15-20 years. Located with on-site parking (entrance on right-hand side). "
    "MANDATORY ENDING: If veneers are mentioned, recommend the Current Promotion button. "
    "Always end by asking if they want to book a free 15-minute virtual consultation or come in-person to get results faster."
)

# 3. ADVANCED TYPING DELAY (5-10 Seconds Based on Length)
def calculate_human_delay(text):
    word_count = len(text.split())
    # Short answers (<25 words) = ~5-6 seconds
    # Medium answers (~50 words) = ~7-8 seconds
    # Long answers (75+ words) = ~9-10 seconds
    base_delay = 5
    additional_time = (min(word_count, 80) / 80) * 5
    total_delay = base_delay + additional_time + random.uniform(-0.5, 0.5)
    return total_delay

# 4. CHAT HISTORY MANAGEMENT
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. MAIN CHAT LOGIC
if prompt := st.chat_input("How can I help you with your smile today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # A. Call Groq
        with st.spinner("Assistant is typing..."):
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                temperature=0.6 # Lower temperature for higher accuracy to rules
            )
            raw_response = completion.choices[0].message.content

            # B. THE SHIELD (Post-processing to fix LLM mistakes)
            # Remove all quotation marks (double and single)
            clean_response = raw_response.replace('"', '').replace("'", "")
            # Force one paragraph by removing any line breaks
            clean_response = " ".join(clean_response.split())

            # C. THE DELAY (Proportional 5-10s)
            delay_time = calculate_human_delay(clean_response)
            time.sleep(delay_time)

            # D. Final Output
            st.markdown(clean_response)
            st.session_state.messages.append({"role": "assistant", "content": clean_response})

# 6. PROMOTION BUTTON (Optional UI Element)
if any("veneer" in m["content"].lower() for m in st.session_state.messages):
    st.sidebar.button("🎁 View Current Veneer Promotion", use_container_width=True)


