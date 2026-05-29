# Headshot AI | Professional Portraits

Generate high-quality professional headshots for LinkedIn, resumes, or corporate profiles using Google's Gemini 2.5 Flash Image ("Nano Banana") model.

## Features (v2.1)
-   **Google-Style UI**: A clean, minimalist, and responsive interface that works beautifully on both desktop and mobile.
-   **Dark Mode Support**: Automatically adjusts based on your system preferences.
-   **Granular Style Controls**: Select specific **Attire**, **Background**, **Lighting**, and **Pose** to customize your look.
-   **Identity Preservation**: Uses specialized Nano Banana models to maintain your facial features while changing your outfit and setting.
-   **Multi-Model Fallback**: High reliability with a tiered attempt strategy (`gemini-2.5-flash-image` -> `gemini-3-pro-image` -> `gemini-2.0-flash`).
-   **Execution Metadata**: View the model used, processing time, and the exact prompt constructed in the sidebar.

## Setup Instructions

1.  **Clone the repository**.
2.  **Install Dependencies**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **API Key Setup**:
    -   Option A: Enter the API key directly in the app's sidebar.
    -   Option B: Create `.streamlit/secrets.toml` and add:
        ```toml
        GEMINI_API_KEY = "your_api_key_here"
        ```
4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Technology Stack
-   **Frontend**: Streamlit
-   **AI Model**: Google Gemini (Nano Banana) via `google-genai` SDK
-   **Image Processing**: Pillow
