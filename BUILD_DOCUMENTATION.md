# Build Documentation: Headshot AI (v2.4)

This document provides a comprehensive guide on how to build, optimize, and extend the **Headshot AI** application. The app leverages Google's Gemini "Nano Banana" models to transform casual photos into professional portraits.

---

## 1. Architectural Overview

The application is built using a **Serverless-Style Frontend** approach:
-   **Frontend**: Streamlit (Python) for a responsive, Google-styled UI.
-   **AI Engine**: Google GenAI SDK (`google-genai`) targeting `gemini-2.5-flash-image`.
-   **State Management**: Streamlit Session State for metadata persistence and UI resets.

---

## 2. Core Implementation Steps

### Prerequisites
- Python 3.10+
- A Google Gemini API Key.

### Step 1: Environment Setup
1. Create a virtual environment: `python3 -m venv .venv`
2. Install dependencies: `pip install streamlit google-genai Pillow python-dotenv`
3. Configure Secrets: Create `.streamlit/secrets.toml` to store the `GEMINI_API_KEY`.

### Step 2: UI Design (Google Minimalism)
The UI follows Google's design language:
-   **Typography**: Google Sans.
-   **Layout**: Centered, responsive container.
-   **Interaction**: Tabbed configuration (Quick Styles vs. Advanced) to reduce cognitive load.

---

## 3. Optimization Techniques (The "Efficiency Stack")

Headshot AI v2.4 implements four layers of optimization to ensure speed and cost-effectiveness.

### Layer 1: Network Optimization (Local Pre-processing)
**Problem**: Modern smartphone photos are 10MB+. Sending these raw files to an API causes high latency and potential timeouts.
**Solution**: 
-   **Resizing**: Images are locally downscaled to a max dimension of 1024px (Balanced/Pro) or 512px (Eco).
-   **Compression**: Images are converted to JPEG with 85% quality before the API call, reducing the payload size by up to 90%.

### Layer 2: Token Optimization (Input Savings)
**Problem**: Default image processing in Gemini uses "Pan and Scan" tiling, costing ~1,032 tokens per image.
**Solution**:
-   **Media Resolution Scaling**: We leverage the `media_resolution` parameter.
    -   `Eco Mode`: Uses `MEDIA_RESOLUTION_LOW` (64 tokens).
    -   `Balanced Mode`: Uses `MEDIA_RESOLUTION_MEDIUM` (256 tokens).
-   **Prompt Engineering**: System instructions are used to define the "Photographer" role once, allowing the user prompt to be a concise, keyword-based string (e.g., `Pose: 3/4. Attire: Suit.`), saving additional input tokens.

### Layer 3: Cost Optimization (Output Savings)
**Problem**: Models may generate unnecessary text metadata or descriptions.
**Solution**:
-   **Output Capping**: `max_output_tokens` is set to 100. Since we only need the image part, this prevents the model from "chattering" and consuming unnecessary output tokens.

### Layer 4: Architectural Optimization (Client Caching)
**Problem**: Instantiating the API client on every Streamlit rerun adds overhead.
**Solution**: 
-   **Resource Caching**: The `genai.Client` is wrapped in `@st.cache_resource`, ensuring it is instantiated once and reused across the session.

---

## 4. User Features & Options

The application provides granular control to the user:

| Category | Options Provided |
| :--- | :--- |
| **Attire** | Navy Suit, Charcoal Suit, Blazer, Smart Sweater, Lab Coat, Business Formal. |
| **Background** | Minimal Studio, Modern Office, City View, Library, Garden, Solid White. |
| **Lighting** | Soft Studio, Rembrandt, Natural Window, Office Bright, Golden Hour. |
| **Pose** | Facing Directly, 3/4 Glance, Confident Tilt, Crossed Arms, Hand on Chin. |
| **Quality Modes** | **Eco** (Fast/Cheap), **Balanced** (Standard), **Pro** (High Detail). |
| **Advanced** | Custom text enhancements (e.g., "Wearing glasses", "Subtle smile"). |

---

## 5. Reliability & Fallback Strategy

To ensure a 99%+ success rate, the app implements a **Tiered Model Fallback**:
1.  **Primary**: `gemini-2.5-flash-image` (The "Nano Banana" sweet spot).
2.  **Secondary**: `gemini-3-pro-image` (High-fidelity fallback).
3.  **Tertiary**: `gemini-2.0-flash` (General multimodal fallback).

If all attempts fail, the app surfaces detailed error logs to the user for troubleshooting (Quota, Safety Filters, etc.).

---

## 6. Future Extensibility
-   **Batch Processing**: Allow users to upload 5-10 photos at once.
-   **Face Consistency fine-tuning**: Utilizing up to 14 reference images (Gemini API capability).
-   **Video Portraits**: Leveraging Gemini's video-to-video capabilities for professional "About Me" clips.
