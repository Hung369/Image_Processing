
# Basic Digital Image Processing

This repo cotains all the source code for Digital Image Processing algorithms. Also a web app demo using Streamlit platform.

## Functionalities
My photoshop web app has these following tasks:
- RGB to Grayscale image, RGB to Sepia image.
- Change image's brightness, contrast values.
- Flip image vertically.
- Circle crop and center crop images.
- Image compression(using PCA algorithms).
- Image edge detection(using Canny algorithms).

## Dependencies
* Python 3.10 - 3.11 is needed for this program.
* OS: Windows 10 - 11
## Installation
First download/clone this repo to your computer
```bash
  git clone https://github.com/Hung369/Image_Processing.git
```
Then create Python virtual environment in the folder that you have cloned and activate it.

In order to deploy the web app, you have to install the project with these following libraries in virtual environment (venv):

```bash
  pip install opencv-python
  pip install numpy
  pip install -U scikit-learn
  pip install streamlit
  pip install Pillow
  pip install pyautogui
```
    
## Deployment

After activating virtual environment and installing all necessary libraries, use bellow command to run the program

```bash
  streamlit run your_script.py
```
## Demo

Demo Link: 


## Acknowledgements
All basic image processing algorithms is in `code from strach` folder. In that folder, all algorithms will be displayed and explained clearly and detailed in each `.ipynb` files. Due to good performance, most of algorithms run on Streamlit website (.py files) is implemented by built-in functions.


## Authors

[@manhhung](https://github.com/Hung369)

