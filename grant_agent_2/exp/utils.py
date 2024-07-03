import os
import glob

def find_pdf_docx(folder_path):
    os.chdir(folder_path)
    pdf_files = glob.glob("*.pdf")
    docx_files = glob.glob("*.docx")
    all_files = pdf_files + docx_files
    all_files = [f"{folder_path.rstrip('/')}/{file}" for file in all_files]
    return all_files