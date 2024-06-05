from fastapi import FastAPI
import os
import requests
import pdfplumber
import pytesseract

app = FastAPI()

def get_all_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


@app.get("/get-message")
async def get_message():
        return {"Message" : "Hello World!"}

@app.get("/getPaths")
async def get_paths():
        paths = []
        folder_path = r'C:\Users\Nemanja\Desktop\StudentRequests'
        all_file_paths = get_all_file_paths(folder_path)
        for path in all_file_paths:
                paths.append(path)
        return {"Paths:" : paths}

@app.get("/readDox")
async def read_dox():
        lines = []
        folder_path = r'C:\Users\Nemanja\Desktop\StudentRequests'
        all_file_paths = get_all_file_paths(folder_path)
        for path in all_file_paths:       
                invoice_pdf = path
                last_three_chars = invoice_pdf[-3:]
                if last_three_chars == "pdf":
                        os.system(f'ocrmypdf --force-ocr {invoice_pdf} output.pdf')
                        with pdfplumber.open("output.pdf") as pdf:
                                page = pdf.pages[0]
                                text = page.extract_text()
                        lines += text.split('\n')
        return lines
                