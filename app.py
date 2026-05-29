import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Headshot AI | Professional Profiles",
    page_icon="👤",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'execution_metadata' not in st.session_state:
    st.session_state.execution_metadata = None
if 'show_api_key_input' not in st.session_state:
    st.session_state.show_api_key_input = False
if 'last_uploaded_filename' not in st.session_state:
    st.session_state.last_uploaded_filename = None

# --- Optimization Helpers ---

@st.cache_resource
def get_gemini_client(api_key):
    """Caches the Gemini Client to avoid re-instantiation on every rerun."""
    return genai.Client(api_key=api_key)

def optimize_image(img, max_dim=1024):
    """Resizes an image to reduce network latency while preserving enough detail for the AI."""
    width, height = img.size
    if max(width, height) > max_dim:
        ratio = max_dim / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        return img.resize(new_size, Image.LANCZOS)
    return img

# --- Google-Style Minimalist CSS ---
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Google Sans', sans-serif;
    }

    .main {
        background-color: transparent;
    }

    /* Minimalist Header */
    .header-container {
        text-align: center;
        padding: 2rem 0 3rem 0;
    }
    .header-title {
        font-weight: 700;
        font-size: 2.5rem;
        color: #1a73e8; /* Google Blue */
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        font-size: 1.1rem;
        color: #5f6368;
    }

    /* Card Styling for Sections */
    .st-emotion-cache-1r6slb0 {
        border-radius: 12px;
        border: 1px solid #dadce0;
        padding: 1.5rem;
        background-color: white;
    }

    /* Dark Mode Adjustments */
    @media (prefers-color-scheme: dark) {
        .header-subtitle { color: #bdc1c6; }
        .st-emotion-cache-1r6slb0 {
            background-color: #202124;
            border-color: #3c4043;
        }
    }

    /* Primary Button - Google Blue */
    div.stButton > button:first-child {
        background-color: #1a73e8;
        color: white;
        border-radius: 24px;
        padding: 0.6rem 2rem;
        font-weight: 500;
        border: none;
        width: 100%;
        transition: box-shadow 0.2s;
    }
    div.stButton > button:first-child:hover {
        box-shadow: 0 1px 3px 1px rgba(60,64,67,.15), 0 1px 2px 0 rgba(60,64,67,.30);
        background-color: #1765cc;
    }

    /* Secondary/Download Button */
    div.stDownloadButton > button:first-child {
        background-color: transparent;
        color: #1a73e8;
        border: 1px solid #dadce0;
        border-radius: 24px;
        width: 100%;
    }
    div.stDownloadButton > button:first-child:hover {
        background-color: rgba(26,115,232,0.04);
        border-color: #1a73e8;
    }

    /* Hide Sidebar elements for cleaner look */
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

def main():
    # --- Header Section ---
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown('<div class="header-title">Headshot AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Professional portraits in seconds, powered by Nano Banana.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar for Keys and Metadata
    with st.sidebar:
        st.title("Settings & Status")
        
        # API Key Management
        stored_key = st.secrets.get("GEMINI_API_KEY", "")
        if st.session_state.show_api_key_input or not stored_key:
            api_key = st.text_input("Gemini API Key", type="password", value=stored_key)
            if st.button("Save & Hide Key"):
                st.session_state.show_api_key_input = False
                st.rerun()
        else:
            st.success("API Key is securely configured.")
            if st.button("Change API Key"):
                st.session_state.show_api_key_input = True
                st.rerun()
            api_key = stored_key

        st.divider()
        
        # Execution Details Section
        st.subheader("Last Execution Details")
        if st.session_state.execution_metadata:
            meta = st.session_state.execution_metadata
            st.write(f"**Model:** `{meta['model']}`")
            st.write(f"**Time:** `{meta['time']:.2f}s`")
            with st.expander("View Full Prompt"):
                st.caption(meta['prompt'])
        else:
            st.caption("No generation data yet.")
        
        st.divider()
        st.caption("v2.2 | Optimized Image Pipeline")

    if not api_key:
        st.warning("Please provide an API key in the sidebar settings.")
        return

    # Using the cached client
    client = get_gemini_client(api_key)

    # --- Main Content: Centered Layout ---
    
    # Section 1: Upload
    with st.container():
        st.markdown("### 1. Source Photo")
        uploaded_file = st.file_uploader("Drop your casual photo here", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        if uploaded_file:
            # Detect new file upload and clear old results
            if st.session_state.last_uploaded_filename != uploaded_file.name:
                st.session_state.execution_metadata = None
                st.session_state.last_uploaded_filename = uploaded_file.name

            input_image_raw = Image.open(uploaded_file)
            st.image(input_image_raw, use_container_width=True)
            st.success("Photo uploaded successfully.")
        else:
            st.info("Tip: Close-up photos with clear lighting work best.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 2: Style Configuration
    if uploaded_file:
        with st.container():
            st.markdown("### 2. Configure Profile")
            
            tab1, tab2 = st.tabs(["Quick Styles", "Advanced"])
            
            with tab1:
                col_a, col_b = st.columns(2)
                with col_a:
                    attire = st.selectbox("Attire", [
                        "Dark Navy Suit", "Charcoal Grey Suit", "Black Blazer", 
                        "Smart Sweater", "Professional Lab Coat", "Business Formal"
                    ])
                    background = st.selectbox("Background", [
                        "Minimal Studio", "Modern Office", "City View (Blurred)", 
                        "Library", "Garden", "Solid White"
                    ])
                with col_b:
                    lighting = st.selectbox("Lighting", [
                        "Soft Studio", "Rembrandt", "Natural Window", 
                        "Office Bright", "Golden Hour"
                    ])
                    pose = st.selectbox("Pose", [
                        "Facing Directly", "3/4 Glance", "Confident Tilt", 
                        "Crossed Arms", "Hand on Chin"
                    ])

            with tab2:
                extra_details = st.text_input("Custom enhancements", 
                                             placeholder="e.g., Wearing black-rimmed glasses, soft smile...")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Prompt Construction: Optimized for low token count
            user_prompt = f"Professional headshot. Pose: {pose.lower()}. Attire: {attire.lower()}. BG: {background.lower()}. Light: {lighting.lower()}. 8k, sharp focus, preserve identity."
            
            if extra_details:
                user_prompt += f" Details: {extra_details}."

            generate_btn = st.button("Generate Professional Portrait")

        # --- Generation Phase ---
        if generate_btn:
            start_time = time.time()
            with st.status("AI is processing...", expanded=False) as status:
                
                # OPTIMIZATION: Resize image before sending to API
                st.write("Optimizing image payload...")
                input_image = optimize_image(input_image_raw)
                
                models_to_try = ["gemini-2.5-flash-image", "gemini-3-pro-image", "gemini-2.0-flash"]
                generated_image = None
                success_model = None
                error_logs = []
                
                for model_id in models_to_try:
                    try:
                        st.write(f"Attempting with {model_id}...")
                        response = client.models.generate_content(
                            model=model_id,
                            contents=[user_prompt, input_image],
                            config=types.GenerateContentConfig(
                                system_instruction="Maintain subject identity. Transform photo to professional headshot strictly following attire, pose, and background.",
                                response_modalities=["Image"],
                                max_output_tokens=100 
                            )
                        )
                        for part in response.candidates[0].content.parts:
                            if part.inline_data:
                                generated_image = Image.open(io.BytesIO(part.inline_data.data))
                                success_model = model_id
                                break
                        if generated_image:
                            break
                    except Exception as e:
                        error_logs.append(f"Model {model_id} failed: {str(e)}")
                        continue
                
                if generated_image:
                    end_time = time.time()
                    # Store metadata and image in session state
                    st.session_state.execution_metadata = {
                        "model": success_model,
                        "time": end_time - start_time,
                        "prompt": user_prompt,
                        "image": generated_image
                    }
                    status.update(label=f"Generation Complete ({success_model})", state="complete", expanded=False)
                    st.rerun()
                else:
                    status.update(label="Generation Failed", state="error", expanded=True)
                    st.error("All model attempts failed to generate an image.")
                    with st.expander("View Error Details"):
                        for log in error_logs:
                            st.write(log)

    # Display Result from session state
    if st.session_state.execution_metadata and 'image' in st.session_state.execution_metadata:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 3. Final Result")
        st.image(st.session_state.execution_metadata['image'], use_container_width=True)
        
        # Download Action
        buf = io.BytesIO()
        st.session_state.execution_metadata['image'].save(buf, format="PNG")
        st.download_button(
            label="Download Portrait",
            data=buf.getvalue(),
            file_name="professional_headshot.png",
            mime="image/png"
        )

    # --- Footer ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #9aa0a6; font-size: 0.8rem;'>Built with Gemini Nano Banana & Streamlit</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
