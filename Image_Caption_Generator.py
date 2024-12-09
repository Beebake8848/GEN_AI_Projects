import streamlit as st
import google.generativeai as genai
from api_key import api_key
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure Google API with the API key
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }
)

# Define the system prompt template
system_prompt_template = """
As a creative AI specializing in generating fun and engaging social media captions, your task is to create short, catchy, and appealing captions that are perfect for sharing on platforms like Instagram, Twitter, and Facebook.

Your responsibilities include:

1. Image Interpretation: Identify the key elements of the image—people, places, objects, or actions—and create a caption that resonates with social media users.
2. Tone and Style: Use a {mood} tone to make the caption engaging and appropriate for the mood selected. The caption should reflect the mood of {mood}. Ensure that the tone and content match this mood. Keep it short, engaging, and relevant to the selected mood.
3. Social Media Appeal: Keep the caption brief (1-2 sentences) with a strong, shareable quality. It should catch attention and spark engagement (likes, comments, shares).
4. Hashtags and Emojis: Where appropriate, include relevant hashtags and emojis to make the caption more interactive and fun.

Important Notes:

1. Be Creative: Go beyond just describing what’s in the image. Add personality, humor, or emotion to match the selected mood.
2. Avoid Over-explaining: Social media captions are short and snappy, so avoid long descriptions. Focus on the mood or essence of the image.
3. Engagement: Consider asking a question or encouraging interaction based on the {mood}.
"""

# Streamlit app configuration
st.set_page_config(page_title="Image Caption Generator with Moods", page_icon=":robot:")

st.title("🖼️ Image Caption Generator with Mood Options")
st.subheader("Select a mood to generate creative social media captions for your images.")

# File uploader for image input
uploaded_file = st.file_uploader("Upload the image for analysis", type=["png", "jpg", "jpeg"])

# Mood selection using radio buttons
mood = st.radio(
    "Select the mood for your caption:",
    ["Funny", "Inspirational", "Casual", "Exciting", "Sweet", "Sarcastic", "Witty"]
)

# Generate caption button
if st.button("Generate Caption"):
    if uploaded_file is not None:
        # Read the image data
        image_data = uploaded_file.getvalue()
        
        # Display the image
        st.image(image_data, width=250)

        # Customize the prompt based on the selected mood
        system_prompt = system_prompt_template.format(mood=mood.lower())
        
        prompt_parts = [
            {"mime_type": "image/jpeg", "data": image_data},  # Adjust MIME type based on uploaded image type
            system_prompt,
        ]

        try:
            # API call to generate caption
            response = model.generate_content(prompt_parts)
            
            # Log the entire response for debugging
            #st.write("Full API Response:", response)

            # Check if the response has text
            if hasattr(response, 'text'):
                caption = response.text  # Use direct attribute access
            elif hasattr(response, 'generated_text'):
                caption = response.generated_text  # Adjust based on the logged structure
            else:
                st.error("Caption not found in response.")
            
            st.write(caption)
        except Exception as e:
            st.error(f"Error generating caption: {str(e)}")
    else:
        st.warning("Please upload an image first!")
