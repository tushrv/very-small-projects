import streamlit as st
import requests
import json

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000/summarize/"

# Streamlit UI
st.title("📝 Text Summarization and Keyword Extraction")
st.write("Enter a paragraph of text, and get a concise summary along with important keywords!")

# Text input
text_input = st.text_area("Input Text", height=200)

if st.button("Summarize and Extract Keywords"):
    if text_input.strip():
        # Escape special characters in the text
        payload = json.dumps({"text": text_input})
        
        # Call FastAPI backend
        headers = {"Content-Type": "application/json"}
        response = requests.post(BACKEND_URL, data=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            st.subheader("Summary")
            st.write(result["summary"])
            st.subheader("Keywords")
            st.write(", ".join(result["keywords"]))
        else:
            st.error(f"Error processing the text. Status code: {response.status_code}")
    else:
        st.warning("Please enter some text to summarize.")