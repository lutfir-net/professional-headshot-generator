import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import os

# Page Configuration
st.set_page_config(
    page_title="Professional Headshot Generator",
    page_icon="📸",
    layout="wide"
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #28a745;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("📸 Professional Headshot Generator")
    st.markdown("Transform your casual photos into professional headshots for LinkedIn, resumes, or corporate profiles using **Nano Banana (Gemini 2.5 Flash Image)**.")

    # Sidebar for API Configuration and Info
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("Enter Gemini API Key", type="password", value=st.secrets.get("GEMINI_API_KEY", ""))
        
        st.info("The app uses 'gemini-2.5-flash-image' (Nano Banana) for high-speed, identity-preserving image editing.")
        
        st.divider()
        st.markdown("### How to use:")
        st.write("1. Upload a clear photo of your face.")
        st.write("2. Describe your desired professional look.")
        st.write("3. Click 'Generate Headshot'.")

    if not api_key:
        st.warning("Please provide a Gemini API Key in the sidebar to proceed.")
        return

    # Initialize Gemini Client
    client = genai.Client(api_key=api_key)

    # UI Layout: Two columns for input and output
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Upload Your Photo")
        uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            input_image = Image.open(uploaded_file)
            st.image(input_image, caption="Original Photo", use_container_width=True)

    with col2:
        st.subheader("2. Customize Your Style")
        
        # Granular Style Controls
        attire = st.selectbox("Professional Attire:", [
            "Dark Navy Suit with White Shirt",
            "Charcoal Grey Suit with Light Blue Shirt",
            "Black Blazer with Professional Top",
            "Beige Smart-Casual Blazer",
            "Professional Doctor's Lab Coat",
            "Casual Professional Sweater",
            "Business Formal with Tie"
        ])

        background = st.selectbox("Background Setting:", [
            "Solid Neutral Grey (Studio)",
            "Soft Blurred Modern Office",
            "Modern Glass Building Lobby",
            "Library with Blurred Bookshelf",
            "Minimalist White Professional Studio",
            "Warm Wooden Interior",
            "Soft Natural Outdoor Garden"
        ])

        lighting = st.selectbox("Lighting Style:", [
            "Studio Softbox Lighting",
            "Rembrandt (Dramatic) Lighting",
            "Natural Window Light",
            "Bright Professional Office Light",
            "Warm Golden Hour Glow"
        ])

        pose = st.selectbox("Subject Pose:", [
            "Facing Camera Directly",
            "3/4 Glance (Slightly Turned)",
            "Profile View (Side Glance)",
            "Dynamic Tilt (Confident Pose)",
            "Crossed Arms (Professional)",
            "Hand on Chin (Thoughtful)"
        ])

        # Advanced options (optional)
        with st.expander("Advanced Prompting"):
            extra_details = st.text_input("Additional details (optional):", 
                                         placeholder="e.g., wearing glasses, subtle smile, specific tie color...")

        # Construct the dynamic prompt
        user_prompt = f"Professional headshot of the person in the image. " \
                      f"The person is {pose.lower()}. " \
                      f"They are wearing a {attire.lower()}. " \
                      f"The background is a {background.lower()}. " \
                      f"The lighting is {lighting.lower()}. " \
                      f"Ensure high-quality, sharp focus, 8k resolution, maintaining the original person's facial features and identity."
        
        if extra_details:
            user_prompt += f" Additional details: {extra_details}."

        st.info(f"**Generated Prompt:** _{user_prompt}_")

        generate_btn = st.button("Generate Headshot")

    if generate_btn:
        if not uploaded_file:
            st.error("Please upload a photo first.")
        elif not user_prompt:
            st.error("Please provide a style description.")
        else:
            with st.spinner("Nano Banana is crafting your professional headshot..."):
                # Model Fallback Strategy
                models_to_try = [
                    "gemini-2.5-flash-image",  # Primary Nano Banana
                    "gemini-3-pro-image",      # Nano Banana Pro
                    "gemini-2.0-flash"         # General Multimodal Fallback
                ]
                
                generated_image = None
                success_model = None
                error_logs = []

                for model_id in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=model_id,
                            contents=[user_prompt, input_image],
                            config=types.GenerateContentConfig(
                                response_modalities=["Image"]
                            )
                        )
                        
                        # Extract the generated image from the response
                        for part in response.candidates[0].content.parts:
                            if part.inline_data:
                                generated_image = Image.open(io.BytesIO(part.inline_data.data))
                                success_model = model_id
                                break
                        
                        if generated_image:
                            break # Successfully generated
                            
                    except Exception as e:
                        error_logs.append(f"{model_id}: {str(e)}")
                        continue # Try the next model
                
                if generated_image:
                    st.success(f"Success! Generated using model: `{success_model}`")
                    st.subheader("3. Your Professional Headshot")
                    st.image(generated_image, caption="Generated Headshot", use_container_width=True)
                    
                    # Download button
                    buf = io.BytesIO()
                    generated_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="Download Headshot",
                        data=byte_im,
                        file_name="professional_headshot.png",
                        mime="image/png"
                    )
                else:
                    st.error("All model attempts failed to generate an image.")
                    with st.expander("View Error Details"):
                        for log in error_logs:
                            st.write(log)
                    st.info("Tip: Ensure your API key is valid and you have sufficient quota for these models.")

if __name__ == "__main__":
    main()
