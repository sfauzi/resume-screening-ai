"""
PDF PARSER UTILITY
Fungsi: Extract teks dari file PDF
"""

import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF file
    
    Args:
        pdf_path (str): Path ke file PDF
        
    Returns:
        str: Text yang diekstrak dari PDF
    """
    try:
        text = ""
        
        # Buka file PDF dalam mode binary
        with open(pdf_path, 'rb') as file:
            # Buat PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Loop melalui setiap halaman
            for page_num in range(len(pdf_reader.pages)):
                # Extract text dari halaman
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        # Clean up text (remove extra spaces and newlines)
        text = ' '.join(text.split())
        
        return text
        
    except Exception as e:
        print(f"Error extracting PDF: {str(e)}")
        return ""

def get_pdf_info(pdf_path):
    """
    Get information about PDF file
    
    Args:
        pdf_path (str): Path ke file PDF
        
    Returns:
        dict: Informasi PDF
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            info = {
                'num_pages': len(pdf_reader.pages),
                'is_encrypted': pdf_reader.is_encrypted
            }
            return info
    except:
        return {'num_pages': 0, 'is_encrypted': False}