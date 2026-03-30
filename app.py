

import streamlit as st
import requests
from openai import OpenAI
from fpdf import FPDF
import io
import re

# --- 1. THE ARCHITECTURAL BLUEPRINT (PDF Class) ---
class DigitalProduct(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def add_chapter(self, title, content):
        self.add_page()
        # "Wealth & Empowerment" Aesthetic: Gold Header
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(184, 134, 11) 
        self.cell(0, 20, title, 0, 1, "L")
        self.ln(5)
        
        # Professional Body: Charcoal Grey
        self.set_font("Helvetica", "", 12)
        self.set_text_color(51, 51, 51)
        self.multi_cell(0, 10, content)

# --- 2. THE AUTOMATED GATEKEEPER (Gumroad Auth) ---
st.set_page_config(page_title="FabFlow AI | Member Access", page_icon="✨", layout="wide")

# Custom CSS for Luxury Branding
st.markdown("""
    <style>
    .stApp { background-color: #FCF9F2; }
    h1, h2, h3 { color: #B8860B; font-family: 'Georgia', serif; }
    .stButton>button { background-color: #B8860B; color: white; border-radius: 25px; border: none; padding: 10px 25px; }
    .stProgress > div > div > div > div { background-color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def verify_license(license_key):
    """Verify key with Gumroad API and print debug info"""
    product_id ="ffbjm" # Ensure this is your actual ID
    url = "https://api.gumroad.com/v2/licenses/verify"
    params = {"product_id": product_id, "license_key": license_key}
    
    try:
        response = requests.post(url, data=params)
        data = response.json()
        
        # --- DEBUG SECTION ---
        # This will show up in your app only when you try to log in
        if not data.get("success"):
            st.warning(f"DEBUG INFO: Gumroad says '{data.get('message')}'")
            st.write("Checking ID:", product_id)
        # ---------------------
        
        return data.get("success", False)
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return False


# --- LOGIN SCREEN ---
if not st.session_state.authenticated:
    st.write("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.title("✨ FabFlow AI")
    st.write("### Founder's Suite Access")
    st.write("Please enter your unique license key to unlock your digital empire.")
    
    user_key = st.text_input("License Key", type="password", placeholder="XXXX-XXXX-XXXX-XXXX")
    
    if st.button("Unlock My Flow"):
        if verify_license(user_key):
            st.session_state.authenticated = True
            st.success("Access Granted. Welcome, Visionary.")
            st.rerun()
        else:
            st.error("License not found. Please check your purchase receipt.")
    
    st.write("---")
    # REPLACE with your actual sales page link
    st.write("[Purchase Access to FabFlow AI](https://gumroad.com/l/your-link)")
    st.write("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. THE AUTHORIZED APP ENGINE ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

st.write("<div style='text-align: center;'><h1>FabFlow AI</h1><p>The Mastermind Suite for Digital Creators.</p></div>", unsafe_allow_html=True)
st.progress(st.session_state.step / 5)

# STEP 1: VOICE CLONING
if st.session_state.step == 1:
    st.subheader("Step 1: Capture Your Essence")
    sample = st.text_area("Paste a writing sample to clone your voice:", height=200)
    if st.button("Continue to Research"):
        if sample:
            st.session_state.data['voice'] = sample
            st.session_state.step = 2
            st.rerun()

# STEP 2: M&M RESEARCH
elif st.session_state.step == 2:
    st.subheader("Step 2: Model Viral Success")
    m_source = st.text_area("Paste Viral Script / Source Material")
    col1, col2 = st.columns([1, 5])
    if col1.button("Back"): 
        st.session_state.step = 1
        st.rerun()
    if col2.button("Design Your Product"):
        st.session_state.data['source'] = m_source
        st.session_state.step = 3
        st.rerun()

# STEP 3: TOPIC & VIBE
elif st.session_state.step == 3:
    st.subheader("Step 3: Define Your Masterpiece")
    title = st.text_input("Product Title")
    outline = st.text_area("Outline (Chapters - one per line)")
    col1, col2 = st.columns([1, 5])
    if col1.button("Back"):
        st.session_state.step = 2
        st.rerun()
    if col2.button("Begin Synthesis"):
        st.session_state.data['title'] = title
        st.session_state.data['outline'] = outline
        st.session_state.step = 4
        st.rerun()

# STEP 4: SYNTHESIS
elif st.session_state.step == 4:
    st.subheader("Step 4: Synthesis in Progress")
    with st.spinner("Our AI artisans are weaving your voice into your product..."):
        voice = st.session_state.data['voice']
        topic = st.session_state.data['title']
        full_content = []
        for chap in st.session_state.data['outline'].split('\n'):
            if chap.strip():
                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": f"Clone this voice: {voice}"},
                              {"role": "user", "content": f"Write a high-value chapter for '{chap}' for '{topic}'."}]
                )
                full_content.append((chap, res.choices[0].message.content))
        st.session_state.data['final_content'] = full_content
        st.success("Synthesis Complete.")
        if st.button("Launch My Product"):
            st.session_state.step = 5
            st.rerun()

# STEP 5: THE LAUNCH (Universal Download Fix)
elif st.session_state.step == 5:
    st.subheader("✨ Your Fabulous Launch Kit")
    pdf = DigitalProduct()
    for title, body in st.session_state.data['final_content']:
        pdf.add_chapter(title, body)
    
    # Universal PDF Buffer
    pdf_output = pdf.output(dest='S').encode('latin-1')
    pdf_buffer = io.BytesIO(pdf_output)
    
    t1, t2 = st.tabs(["📄 Download Product", "📱 Marketing Strategy"])
    with t1:
        st.download_button(
            label="📥 Download PDF Masterpiece",
            data=pdf_buffer,
            file_name=f"{st.session_state.data['title']}.pdf",
            mime="application/pdf",
            key="final-download-btn"
        )
    with t2:
        st.write("### Marketing Plan")
        st.info("Content strategies tailored to your cloned voice are ready for use.")

    if st.button("Create Another Empire"):
        st.session_state.step = 1
        st.session_state.data = {}
        st.rerun()
