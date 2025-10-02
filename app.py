import streamlit as st
import requests
import json

# ===== CONFIGURATION =====
PROJECT_ID = "predictors-group-project"        # ← Replace with your GCP project ID
ENDPOINT_ID = "893747922242371584"      # ← Replace with your Vertex AI endpoint ID
LOCATION = "us-central1"

# ===== HELPER FUNCTION =====
def predict_specialty(text_input):
    import subprocess
    import requests

    # Get access token
    token = subprocess.getoutput("gcloud auth print-access-token").strip()

    # ✅ USE THE DEDICATED ENDPOINT URL FROM THE ERROR MESSAGE
    DEDICATED_DOMAIN = "893747922242371584.us-central1-624188742397.prediction.vertexai.goog"
    
    url = f"https://{DEDICATED_DOMAIN}/v1/projects/predictors-group-project/locations/us-central1/endpoints/893747922242371584:predict"

    payload = {
        "instances": [text_input]
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["predictions"][0]
    else:
        return f"Error: {response.status_code} - {response.text}"

# ===== STREAMLIT UI =====
st.set_page_config(page_title="MedArchive Classifier", page_icon="🏥")
st.title("🏥 MedArchive Clinical Document Classifier")
st.markdown("Enter a clinical transcription to predict its medical specialty.")

# Text input
user_input = st.text_area(
    "Clinical Transcription",
    height=150,
    placeholder="e.g., Patient presents with acute chest pain, shortness of breath, and ECG shows ST elevation..."
)

# Predict button
if st.button("Classify Specialty"):
    if user_input.strip():
        with st.spinner("Predicting..."):
            prediction = predict_specialty(user_input)
        st.success(f"**Predicted Specialty:** {prediction}")
    else:
        st.warning("Please enter a transcription.")

# Footer
st.markdown("---")
st.caption("Powered by Google Cloud Vertex AI • Group Project ITS 2130")