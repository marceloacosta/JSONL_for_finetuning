
# AI Fine Tuning Data Preparation Tool

This tool, powered by Streamlit, allows you to prepare data for fine-tuning AI models. It can read text files (txt, doc, docx, pdf) and use the GPT-4 model to generate a set of questions based on the text. The result is a .jsonl file which is made available for download.

## Dependencies

The tool is dependent on the following Python libraries:

- os
- re
- json
- jsonlines
- base64
- docx
- pdfplumber
- requests
- streamlit
- io

You can install the dependencies using pip:

```bash
pip install python-docx pdfplumber requests streamlit jsonlines
```

## How to Run the Tool

To run the Streamlit app, use the following command in your terminal:

```bash
streamlit run app.py
```

Once the app is running, follow these steps:

1. Enter your GPT-4 API key in the input field. (You can also use a cheaper model, for this you will have to make the necessary changes in the code)
2. Upload a text file in one of the following formats: txt, doc, docx, pdf.
3. Define the chunk size in the respective input field.
4. Press the 'Process' button.

The tool will divide the text into chunks of the specified size and generate questions for each chunk using the GPT-4 model. The results will be written to a .jsonl file and a download link will be provided.

## Code Structure

The main function of the tool is `main()`, which is responsible for the Streamlit interface and the main logic of the tool.

The tool includes several helper functions:

- `read_doc(file_path)`: Reads a .doc or .docx file and returns the text.
- `read_pdf(file_path)`: Reads a .pdf file and returns the text.
- `gpt4_analyze(text, api_key, prompt)`: Sends a request to the GPT-4 API and returns the result.
- `get_text_file_content(file)`: Returns the content of a .txt file.
- `get_chunks(text, chunk_size)`: Divides the text into chunks of the specified size.
- `get_download_link(file_name, text)`: Creates a download link for a file.

Please note: You will need to replace the API key placeholder with your actual OpenAI API key in order to use the GPT-4 model.
