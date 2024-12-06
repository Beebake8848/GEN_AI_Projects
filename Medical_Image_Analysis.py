import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key=api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }
)

system_prompt="""

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential treatment options or interventions.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are "Unable to be determined based on the provided image."
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult a Doctor Before making any decisions..."
Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

"""

st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot")

st.title("👨‍⚕️ Vital Image Analytics")
st.subheader("An application that can help users to identify medical image")
uploaded_file = st.file_uploader("Upload to medical image for analysis", type=["png","jpg","jpeg"])
submit_button = st.button("Generate the analysis")

if submit_button:
    image_data = uploaded_file.getvalue()
    
    image_parts = [
      {
        "mime_type": "image/jpeg",
        "data": image_data
      }
    ]
    
    prompt_parts = [
      image_parts[0],
      system_prompt,
    ]

    response = model.generate_content(prompt_parts)
    st.image(image_data, width=250)
    st.write(response.text)
