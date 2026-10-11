import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Handwriting to Text OCR",
    page_icon="✍️",
    layout="centered"
)

# Application title
st.title("✍️ Handwriting-to-Text OCR")

st.write(
    "Upload an image containing handwritten English text "
    "and convert it into digital text."
)

# Load the OCR model only once
@st.cache_resource
def load_reader():
    return easyocr.Reader(["en"], gpu=False)

# Upload image
uploaded_file = st.file_uploader(
    "Upload your handwritten image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    try:
        # Read image
        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

        # Extract text
        if st.button("Extract Text", type="primary"):

            with st.spinner(
                "Loading OCR model and recognizing text..."
            ):
                reader = load_reader()

                image_array = np.array(image)

                results = reader.readtext(image_array)

                extracted_text = "\n".join(
                    result[1] for result in results
                )

            st.subheader("Extracted Text")

            if extracted_text.strip():

                st.text_area(
                    "Recognized text",
                    value=extracted_text,
                    height=200
                )

                st.download_button(
                    label="Download Extracted Text",
                    data=extracted_text,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )

                st.success("Text extraction completed!")

            else:
                st.warning(
                    "No text was detected. Try a clearer image."
                )

    except Exception as error:
        st.error("Something went wrong while processing the image.")
        st.exception(error)

st.divider()

st.caption(
    "Developed using Python, EasyOCR and Streamlit."
)