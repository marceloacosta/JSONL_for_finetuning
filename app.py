import os
import re
import json
import jsonlines
import base64
from docx import Document
import pdfplumber
import requests
import streamlit as st
from io import BytesIO, StringIO


def read_doc(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def gpt4_analyze(text, api_key, prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    }

    url = "https://api.openai.com/v1/chat/completions"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    result = response.json()

    completion_string = result['choices'][0]['message']['content']

    # Use a regex to find all JSON objects in the string
    json_objects = re.findall(r'\{.*?\}', completion_string)

    # Parse each JSON object and return them as a list
    return [json.loads(obj) for obj in json_objects]



def get_text_file_content(file):
    return file.getvalue().decode()


def get_chunks(text, chunk_size):
    return (text[i: i + chunk_size] for i in range(0, len(text), chunk_size))


def get_download_link(file_name, text):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{file_name}">Download result file</a>'


def main():
    st.title('AI Fine Tuning Data Preparation')

    api_key = st.text_input('Enter your GPT-4 API key')
    file = st.file_uploader("Upload a text file", type=["txt", "doc", "docx", "pdf"])
    chunk_size = st.number_input('Chunk size', value=2000, min_value=500)
    prompt = """
            Please generate 20 appropriate questions for the following text and place the questions and text in JSONL format.
The "completion" should come verbatim from the text. You must use the "you" form for questions. You must utilize the entire text:"
Example:{"prompt":"What is the strategy to adapt if you think you don't have money to save?", "completion":"You say you don't have it, take it off the top and forget it's there. You will adjust and once you adjust, it will provide financial freedom for the long term."} {"prompt":"Why is it important to become an owner and not just a consumer?",
"completion":"First, you've got to get in the game. You've got to become an owner, not just a consumer."}"""

    if st.button('Process'):
        if file is not None:
            file_ext = file.name.split('.')[-1].lower()

            if file_ext == "txt":
                text = get_text_file_content(file)
            elif file_ext == "doc" or file_ext == "docx":
                text = read_doc(file)
            elif file_ext == "pdf":
                text = read_pdf(file)
            else:
                st.write(f"Error: The file format {file_ext} is not supported.")
                return

            output_file_name = "output.jsonl"
            with jsonlines.open(output_file_name, mode='a') as writer:  # open the file in append mode
                for chunk in get_chunks(text, chunk_size):
                    try:
                        results = gpt4_analyze(chunk, api_key, prompt)
                        writer.write_all(results)
                    except Exception as e:
                        st.write(f"Error: {str(e)}. The operation will be resumed from the next chunk.")
                        continue

            with open(output_file_name, "r") as file:
                download_link = get_download_link(output_file_name, file.read())
                st.markdown(download_link, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
