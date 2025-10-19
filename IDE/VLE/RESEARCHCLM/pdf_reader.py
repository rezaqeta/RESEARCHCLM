#!/usr/bin/env python3
"""
Fast PDF Text Extractor
Uses PyMuPDF (fitz) - the fastest PDF text extraction library
"""

import fitz  # PyMuPDF
import sys
import os

def extract_text_fast(pdf_path, output_file=None):
    """
    Extract text from PDF using PyMuPDF (fastest method)
    
    Args:
        pdf_path (str): Path to PDF file
        output_file (str): Optional output text file path
    
    Returns:
        str: Extracted text
    """
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        text = ""
        
        # Extract text from all pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.get_text()
        
        doc.close()
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Text saved to: {output_file}")
        
        return text
        
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_reader.py <pdf_file> [output_file]")
        print("Example: python pdf_reader.py document.pdf extracted_text.txt")
        return
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(pdf_file):
        print(f"PDF file not found: {pdf_file}")
        return
    
    print(f"Extracting text from: {pdf_file}")
    text = extract_text_fast(pdf_file, output_file)
    
    if not output_file:
        print("\n" + "="*50)
        print("EXTRACTED TEXT:")
        print("="*50)
        print(text[:2000] + "..." if len(text) > 2000 else text)

if __name__ == "__main__":
    main()




