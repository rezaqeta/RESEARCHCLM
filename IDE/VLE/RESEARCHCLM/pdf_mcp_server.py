#!/usr/bin/env python3
"""
Simple PDF Reader MCP Server
Provides tools for reading PDF files locally
"""

import json
import sys
import os
from pathlib import Path
from PyPDF2 import PdfReader
import argparse

class PDFReaderMCP:
    def __init__(self):
        self.name = "pdf-reader"
        self.version = "1.0.0"
    
    def read_local_pdf(self, path: str) -> dict:
        """
        Extract text from a local PDF file
        
        Args:
            path (str): Path to the PDF file
            
        Returns:
            dict: JSON response with extracted text or error
        """
        try:
            # Check if file exists
            if not os.path.exists(path):
                return {
                    "success": False,
                    "error": f"File not found: {path}"
                }
            
            # Check if it's a PDF file
            if not path.lower().endswith('.pdf'):
                return {
                    "success": False,
                    "error": f"File is not a PDF: {path}"
                }
            
            # Extract text using PyPDF2
            reader = PdfReader(path)
            text = ""
            
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page_text
                text += "\n"
            
            return {
                "success": True,
                "data": {
                    "text": text.strip(),
                    "page_count": len(reader.pages),
                    "file_path": path
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading PDF: {str(e)}"
            }
    
    def handle_request(self, request: dict) -> dict:
        """
        Handle MCP requests
        
        Args:
            request (dict): MCP request
            
        Returns:
            dict: MCP response
        """
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "read_local_pdf":
                path = arguments.get("path")
                if not path:
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {
                            "code": -32602,
                            "message": "Missing required parameter: path"
                        }
                    }
                
                result = self.read_local_pdf(path)
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }

def main():
    parser = argparse.ArgumentParser(description="PDF Reader MCP Server")
    parser.add_argument("--path", help="Path to PDF file to read")
    args = parser.parse_args()
    
    if args.path:
        # Direct file reading mode
        pdf_reader = PDFReaderMCP()
        result = pdf_reader.read_local_pdf(args.path)
        print(json.dumps(result, indent=2))
        return
    
    # MCP server mode
    pdf_reader = PDFReaderMCP()
    
    # Send initialization response
    init_response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": pdf_reader.name,
                "version": pdf_reader.version
            }
        }
    }
    
    print(json.dumps(init_response))
    sys.stdout.flush()
    
    # Handle requests
    try:
        for line in sys.stdin:
            if line.strip():
                request = json.loads(line)
                response = pdf_reader.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()




