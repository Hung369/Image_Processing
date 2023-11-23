import process
import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
import pyautogui

def uploader():
    file_upload = st.file_uploader("Choose file (only for color image)", type = ['png', 'jpg', 'jpeg'])

    # Condition when uploading a file
    if file_upload is not None:    
        image = Image.open(file_upload)
        img = np.array(image)
        st.image(img,caption='uploaded image')
        return img
    return None

def Display(image):
    if image is not None:
        st.image(image, caption="result")

def Convert(result):
    if result is not None:
        final = Image.fromarray(result.astype('uint8'))
        buf = BytesIO()
        final.save(buf, format='PNG')
        return buf.getvalue()
    return None

# Menu for basic task
def Basic(img):
    radio_btn = st.radio(label="Selection: ", options=["No effect","Grayscale", "Sepia", "Blur", "Circle crop", "Flip", "Center crop"], horizontal=True)
    bval = st.slider(label="Brightness", min_value = -20, max_value = 20, value = 0)
    cval = st.slider(label="Contrast", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

    if radio_btn == "No effect":
        result = img.copy()
            
    if radio_btn == "Grayscale":
        result = process.RGB2Gray(img)

    if radio_btn == "Sepia":
        result = process.RGB2Sep(img)

    if radio_btn == "Blur":
        result = process.BlurImg(img)

    if radio_btn == "Circle crop":
        result = process.CircleCrop(img)
        
    if radio_btn == "Center crop":
        result = process.CropCenter(img)

    if radio_btn == "Flip":
        choice = st.radio(label="Direction",options=["Vertical", "Horizontal"])
        if choice == "Vertical":
            result = process.flipVertical(img)
        if choice == "Horizontal":
            result = process.flipHorizontal(img)
        
    result = process.Contrast(result,cval)
    result = process.Brightness(result,bval)
    return result

if __name__ == "__main__":
    st.title("Photoshop")
    st.markdown("---")
    st.header("Upload your image")
    img = uploader()
    result = None

    option = st.selectbox('How would you like to edit image?',('Basic', 'Edge Detection', 'Image Compression'))

    if img is not None and option is not None:
        if option == 'Basic':
            result = Basic(img)
        if option == 'Edge Detection':
            st.write("Create a pencil sketch for your image by adjust the range below")
            low = high = 0

            col1, col2 = st.columns(2)
            with col1:
                st.write("Low Threshold")
            with col2:
                low = st.number_input("Enter low number")
            
            col3, col4 = st.columns(2)
            with col3:
                st.write("High Threshold")
            with col4:
                high = st.number_input("Enter high number")
            
            result = process.EdgeDetection(img,low,high)

        if option == 'Image Compression':
            rank = st.number_input("Enter rank number ",min_value=50, max_value=200)
            result = process.pca_compressor(img, rank)

        Display(result)
    
    col1, _, _, _, col2 = st.columns(5)
    with col1:
        if st.button("Reset"):
            pyautogui.hotkey("ctrl","F5")
    with col2:
        if result is not None:
            btn = st.download_button(
                label='Download Image',
                data=Convert(result),
                file_name='imagename.png',
                mime='image/png',
            )
    