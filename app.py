#Import Librarires

from dotenv import load_dotenv
load_dotenv()   # load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


# Configure Gemini API Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



# Load Google Gemini API and get response

def get_gemini_response(input_prompt, image):
    
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text



# Read the image and set the image format

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



# Gemini Prompt

input_prompt = """
You are an automobile expert tasked with providing a detailed overview of any vehicles.
The information should be presented in a structured format as follows:

Brand: Name of the vehicle brand.
Model: Specific model of the vehicle.
Launch year: Since when the vehicle is available in market.
Key Features: Describe the engine capacity, type (e.g., scooter, motorcycle, sedan, SUV),
and special features (any top 3).
Mileage: Provide the average mileage in km/l.
Average Price in INR: Mention the price range.
Other Details: Maintenance costs, benefits, and unique selling points.
Approximate Resale Value: Estimate resale value after 10 years in INR.
"""


# Initialize Streamlit App

st.set_page_config(page_title="Welcome")
st.header("AutoSage App")



# Image Upload

uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png"]
)

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


# -------------------------------------
# Submit Button
# -------------------------------------
submit = st.button("Submit")


if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)

    st.header("The details about the Vehicle are as follow:")
    st.write(response)