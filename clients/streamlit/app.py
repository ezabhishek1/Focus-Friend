"""
Focus Friend - Streamlit Dashboard Client.
A secondary Streamlit interface providing an accessible, local dashboard version.
Imports business logic and domain constants directly from the backend service layer.
"""

import streamlit as st
import time
from backend.services.extraction_service import ExtractionService
from backend.constants import OVERWHELM_PRESETS
from backend.exceptions import FocusFriendError, InputValidationError

# Page Configuration
st.set_page_config(
    page_title="FOCUS FRIEND — Local-First Executive Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Neo-Brutalist Custom CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Plus+Jakarta+Sans:wght@600;800;900&family=Space+Grotesk:wght@700;800&display=swap');

    .stApp {
        background-color: #FAF7EE !important;
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
        color: #121212 !important;
    }

    #MainMenu, header, footer {
        visibility: hidden !important;
    }

    .neo-header {
        background: #FFFFFF;
        border: 4px solid #121212;
        box-shadow: 6px 6px 0px #121212;
        padding: 1.25rem 1.75rem;
        margin-bottom: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .neo-brand-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        line-height: 1;
        letter-spacing: -0.03em;
    }

    .neo-brand-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 800;
        color: #4B5563;
        margin-top: 4px;
    }

    .persona-box {
        background: #38BDF8;
        color: #121212;
        border: 3px solid #121212;
        box-shadow: 5px 5px 0px #121212;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.45;
    }

    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #121212 !important;
        border: 3px solid #121212 !important;
        box-shadow: 4px 4px 0px #121212 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        border-radius: 0px !important;
    }

    .stButton > button {
        background-color: #FFE600 !important;
        color: #121212 !important;
        border: 3px solid #121212 !important;
        box-shadow: 5px 5px 0px #121212 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        text-transform: uppercase !important;
        border-radius: 0px !important;
        padding: 0.65rem 1.5rem !important;
    }

    .card-vibe {
        background-color: #E0F2FE;
        border: 4px solid #121212;
        border-top: 12px solid #38BDF8;
        box-shadow: 6px 6px 0px #121212;
        padding: 1.5rem;
        min-height: 220px;
    }

    .card-deadline {
        background-color: #FFE4E6;
        border: 4px solid #121212;
        border-top: 12px solid #FF6B6B;
        box-shadow: 6px 6px 0px #121212;
        padding: 1.5rem;
        min-height: 220px;
    }

    .card-action {
        background-color: #ECFDF5;
        border: 4px solid #121212;
        border-top: 12px solid #A3E635;
        box-shadow: 6px 6px 0px #121212;
        padding: 1.5rem;
        min-height: 220px;
    }

    .card-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 800;
        color: #4B5563;
        margin-bottom: 0.4rem;
        text-transform: uppercase;
    }

    .card-headline {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        color: #121212;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
    }

    .card-content-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        line-height: 1.45;
        color: #121212;
    }

    .action-bullet {
        background: #FFFFFF;
        border: 2px solid #121212;
        box-shadow: 3px 3px 0px #121212;
        padding: 0.85rem;
        margin-top: 0.5rem;
        font-size: 1.15rem;
        font-weight: 900;
    }
</style>
""", unsafe_allow_html=True)

# Header & Persona Callout
st.markdown("""
<div class="neo-header">
    <div>
        <h1 class="neo-brand-title">⚡ FOCUS FRIEND</h1>
        <div class="neo-brand-sub">v1.0 // LOCAL-FIRST EXECUTIVE COMPANION FOR ADHD // STREAMLIT CLIENT</div>
    </div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 800; background: #A3E635; border: 2px solid #121212; padding: 0.4rem 0.8rem; box-shadow: 2px 2px 0px #121212;">
        🔒 0% CLOUD LEAKAGE • 100% PRIVATE
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="persona-box">
    <strong>🎯 Built for Alex ("The Overwhelmed Professional"):</strong>
    Paste any overwhelming wall of text (email, Slack flurry, Discord ping). Focus Friend cuts cognitive noise down to three essentials: <strong>The Vibe</strong>, <strong>The Deadline</strong>, and <strong>The Action Item</strong>.
</div>
""", unsafe_allow_html=True)

# Preset Buttons (Imported from backend.constants)
st.write("**⚡ Overwhelm Presets:**")
cols = st.columns(len(OVERWHELM_PRESETS))
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

for i, (key, preset_data) in enumerate(OVERWHELM_PRESETS.items()):
    btn_label = f"{preset_data['emoji']} {preset_data['title']}"
    if cols[i].button(btn_label, key=f"preset_{key}"):
        st.session_state.input_text = preset_data["text"]

user_input = st.text_area(
    label="Raw Input Buffer",
    value=st.session_state.input_text,
    placeholder="Paste your 4-paragraph email, Slack dump, or panic notification here...",
    height=160,
    label_visibility="collapsed"
)

col_act1, col_act2 = st.columns([1, 4])
extract_btn = col_act1.button("⚡ EXTRACT SIGNAL")
clear_btn = col_act2.button("✕ CLEAR")

if clear_btn:
    st.session_state.input_text = ""
    st.rerun()

if extract_btn:
    clean_input = user_input.strip() if user_input else ""
    if not clean_input:
        st.warning("⚠️ Please paste a message or choose a preset first to extract signal.")
    elif len(clean_input) < 5:
        st.warning("⚠️ Input message must contain at least 5 characters.")
    else:
        try:
            with st.spinner("Filtering cognitive noise and emotional fluff..."):
                time.sleep(0.2)
                res = ExtractionService.distill(clean_input)

            st.markdown("---")
            st.markdown(
                f"<div style='font-family: JetBrains Mono; font-size: 0.85rem; font-weight: 800; margin-bottom: 1rem;'>"
                f"⚡ DISTILLED VIA {res['engine']} ({res['latency_seconds']}s)</div>",
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="card-vibe">
                    <div class="card-tag">01 // EMOTIONAL CONTEXT</div>
                    <div class="card-headline">THE VIBE</div>
                    <div class="card-content-text">"{res['vibe']}"</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="card-deadline">
                    <div class="card-tag">02 // HARD DEADLINE</div>
                    <div class="card-headline">THE DEADLINE</div>
                    <div class="card-content-text">{res['deadline']}</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="card-action">
                    <div class="card-tag">03 // SINGLE NEXT STEP</div>
                    <div class="card-headline">THE ACTION ITEM</div>
                    <div class="action-bullet">➔ {res['action_item']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.success(f"Action ready to copy: **{res['action_item']}**")

        except InputValidationError as err:
            st.error(f"⚠️ Validation Error: {err.message}")
        except FocusFriendError as err:
            st.error(f"⚠️ Engine Error: {err.message}")
        except Exception as err:
            st.error(f"⚠️ An unexpected error occurred: {str(err)}")
