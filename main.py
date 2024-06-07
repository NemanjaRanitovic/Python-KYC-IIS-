import json
from fastapi import FastAPI
import os
import httpx
import requests
import pdfplumber
import pytesseract
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081/","http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Users(BaseModel):
    usernames: str

def get_all_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

@app.post("/studentRequests")
async def read_dox(users : Users):
        lines = []               
        folder_path = rf'C:\Users\Nemanja\Desktop\StudentRequests\{users.usernames}'
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

@app.post("/pensionerRequests")
async def read_dox(users : Users):
        lines = []               
        folder_path = rf'C:\Users\Nemanja\Desktop\PensionerRequests\{users.usernames}'
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
