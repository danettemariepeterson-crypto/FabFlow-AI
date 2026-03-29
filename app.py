import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
from fpdf import FPDF

# --- SETUP & THEME ---
st.set_page_config(page_title="FabFlow AI", page_icon="✨", layout="wide")

# Custom CSS for the "Feminine Wealth" Aesthetic
st.markdown("""
    <style>
    /* Main background and font */
    .stApp {
        background-color: #FCF9F2;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Clean, gold headers */
    h1, h2, h3 {
        color: #B8860B;
        font-weight: 300 !important;
        letter-spacing: 1px;
    }
    /* Empowering Buttons */
    .stButton>button {
        background-color: #B8860B;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #D4AF37;
        transform: translateY(-2px);
    }
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #D4AF37;
    }
    /* Input Cards */
    .css-1r6slb0 {
        border: 1px solid #E0E0E0;
        border-radius: 15px;
        padding: 20px;
        background: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# --- HEADER ---
st.write(f"<div style='text-align: center;'> <h1 style='font-size: 3rem;'>FabFlow AI</h1> <p style='color: #666; font-style: italic;'>Elevating your vision into a digital empire.</p> </div>", unsafe_allow_html=True)

# Progress Tracker
cols = st.columns(5)
steps = ["Voice", "Source", "Design", "Refine", "Launch"]
for i, s in enumerate(steps):
    if st.session_state.step > i:
        cols[i].write(f"✨ **{s}**")
    else:
        cols[i].write(f"<span style='color: #CCC;'>{s}</span>", unsafe_allow_html=True)
st.progress(st.session_state.step / 5)

st.divider()

# --- AUTOMATIC WIZARD FLOW ---

# STEP 1: VOICE CLONING
if st.session_state.step == 1:
    with st.container():
        st.subheader("Step 1: Capture Your Essence")
        st.write("To keep your brand authentic, paste a snippet of your writing below. I'll learn your unique rhythm and grace.")
        voice_sample = st.text_area("Your Writing Sample", height=200, placeholder="Type or paste here...")
        if st.button("Continue to Research"):
            if voice_sample:
                st.session_state.data['voice'] = voice_sample
                next_step()
            else:
                st.warning("Please share a bit of your voice to proceed.")

# STEP 2: M&M RESEARCH (The Source)
elif st.session_state.step == 2:
    with st.container():
        st.subheader("Step 2: Model Viral Success")
        st.write("Link a piece of content that inspires you, or paste a viral script you'd like to recreate with your own flair.")
        url = st.text_input("Viral URL (YouTube/TikTok)")
        manual_script = st.text_area("Or paste a script/hook here")
        
        col1, col2 = st.columns([1, 5])
        if col1.button("Back"): prev_step()
        if col2.button("Design Your Product"):
            st.session_state.data['script'] = manual_script or url
            next_step()

# STEP 3: BRANDING & TOPIC
elif st.session_state.step == 3:
    with st.container():
        st.subheader("Step 3: Define Your Masterpiece")
        topic = st.text_input("What is the title of your high-value product?")
        st.write("Select your aesthetic vibe:")
        vibe = st.select_slider("Aesthetic Direction", options=["Minimalist Luxury", "Organic Chic", "Bold Empowerment", "Classic Elegance"])
        
        col1, col2 = st.columns([1, 5])
        if col1.button("Back"): prev_step()
        if col2.button("Begin Synthesis"):
            st.session_state.data['topic'] = topic
            st.session_state.data['vibe'] = vibe
            next_step()

# STEP 4: GENERATION (The "Waiting Room")
elif st.session_state.step == 4:
    with st.container():
        st.subheader("Step 4: Synthesis in Progress")
        st.write(f"Bringing '{st.session_state.data['topic']}' to life with a {st.session_state.data['vibe']} aesthetic...")
        
        with st.spinner("Our AI artisans are crafting your assets..."):
            # Logic for OpenAI API calls would happen here
            import time
            time.sleep(2) # Simulating generation
            
        st.success("Your Digital Empire is ready for review.")
        if st.button("View My Launch Kit"):
            next_step()

# STEP 5: THE LAUNCH (Final Hub)
elif st.session_state.step == 5:
    st.subheader("✨ Your Fabulous Launch Kit")
    
    tab1, tab2, tab3 = st.tabs(["📄 The Product", "📱 Marketing", "📅 30-Day Plan"])
    
    with tab1:
        st.write("### Your Professional Digital Product")
        st.info("The PDF has been generated with your custom brand kit and voice.")
        st.button("📥 Download PDF Masterpiece")
        
    with tab2:
        st.write("### High-Conversion Funnel & Socials")
        st.markdown("> **Viral Hook Modeled:** *'I used to spend 10 hours a day... now I spend 10 minutes.'*")
        st.write("Your captions have been humanized and tailored to your voice.")

    if st.button("Start Over"):
        st.session_state.step = 1
        st.rerun()
