# Professional Headshot Generator

Generate high-quality professional headshots for LinkedIn or corporate profiles using Google's Gemini 2.5 Flash Image ("Nano Banana") model.

## Setup Instructions

1.  **Clone/Download** this directory.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **API Key Setup**:
    -   Create a file at `HeadshotApp/.streamlit/secrets.toml`.
    -   Add your Gemini API key:
        ```toml
        GEMINI_API_KEY = "your_api_key_here"
        ```
    -   Alternatively, you can enter the API key directly in the app's sidebar.
4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Features
-   **Identity Preservation**: Nano Banana keeps your face consistent while changing your attire and background.
-   **Pre-defined Styles**: Choose from Corporate, Creative, Academic, or Tech Startup looks.
-   **Custom Prompts**: Describe exactly what you want to wear and where you want to be.
-   **Fast Generation**: Get your new headshot in seconds.
