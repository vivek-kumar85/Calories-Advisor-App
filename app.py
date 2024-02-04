import streamlit as st
import google.generativeai as genai
import os 
from dotenv import load_dotenv
load_dotenv() # loading all the environment variable
from PIL import Image 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="SwadFit Advisor App")


st.markdown("<h1 style='text-align: center; padding: 10px; border-bottom: 8px solid #138808;'><span style='color: #FF9933;'>Swad</span><span style='color: #FFFFFF;'>Fit</span><span style='color: #138808;'>Advisor</span></h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #FFA500; font-size: 1.5em; font-weight: bold;'>Upload an image of your meal and get detailed nutrition information!</h2>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
submit=st.button("Tell me the total calories")

input_prompt="""
You are an expert in nutritionist like Ryan Fernando where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               ----
               Total Calories :
               
        Finally you can also mention whether the Food is healthy or not and also mention the 
        percentage of  carbohydrates ,fats , Proteins , fibers, sugar and other important
        things which is there in given Food Items


"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header("The Food Items Are :")
    st.write(response)
    