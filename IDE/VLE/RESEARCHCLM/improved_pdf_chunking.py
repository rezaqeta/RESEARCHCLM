"""
Improved PDF Chunking Script with Better Error Handling
"""

# Apply compatibility fix
exec(open('fix_formatargspec.py').read())

import os
import glob
from pathlib import Path
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from hash_embedding import HashEmbedding
import json
from datetime import datetime
import traceback

# Try multiple PDF readers
try:
    import PyPDF2
    PDF_READER = "PyPDF2"
except ImportError:
    try:
        import pdfplumber
        PDF_READER = "pdfplumber"
    except ImportError:
        try:
            import fitz  # PyMuPDF
            PDF_READER = "fitz"
        except ImportError:
            print("❌ No PDF reader available! Install PyPDF2, pdfplumber, or PyMuPDF")
            exit()

print("="*70)
print("📚 Improved PDF Chunking Script")
print(f"🔧 Using PDF reader: {PDF_READER}")
print("="*70)

# Set up embeddings
Settings.embed_model = HashEmbedding()

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using multiple methods"""
    
    # Method 1: PyPDF2
    if PDF_READER == "PyPDF2":
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"   ⚠️ PyPDF2 failed: {e}")
    
    # Method 2: pdfplumber
    if PDF_READER == "pdfplumber":
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except Exception as e:
            print(f"   ⚠️ pdfplumber failed: {e}")
    
    # Method 3: PyMuPDF (fitz)
    if PDF_READER == "fitz":
        try:
            import fitz
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text() + "\n"
            doc.close()
            return text.strip()
        except Exception as e:
            print(f"   ⚠️ PyMuPDF failed: {e}")
    
    return None

def chunk_pdf(pdf_path, chunk_size=200, chunk_overlap=50):
    """Chunk a single PDF file with better error handling"""
    print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
    
    # Check file size
    try:
        file_size = os.path.getsize(pdf_path)
        if file_size == 0:
            print(f"   ❌ Empty file")
            return None
        if file_size > 50 * 1024 * 1024:  # 50MB
            print(f"   ⚠️ Large file ({file_size/1024/1024:.1f}MB) - skipping")
            return None
    except Exception as e:
        print(f"   ❌ Cannot access file: {e}")
        return None
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    if not text or len(text.strip()) < 100:
        print(f"   ❌ No text extracted or too short")
        return None
    
    # Create document
    doc = Document(text=text)
    
    # Chunk document
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.get_nodes_from_documents([doc])
    
    print(f"   ✅ Extracted {len(text)} characters")
    print(f"   ✅ Created {len(chunks)} chunks")
    
    return {
        'file_path': pdf_path,
        'file_name': os.path.basename(pdf_path),
        'file_size': file_size,
        'text_length': len(text),
        'chunks_count': len(chunks),
        'chunks': [
            {
                'id': chunk.id_,
                'text': chunk.text,
                'metadata': chunk.metadata
            }
            for chunk in chunks
        ]
    }

def process_pdfs_batch(pdf_files, batch_size=20):
    """Process PDFs in smaller batches with progress tracking"""
    
    all_results = []
    failed_files = []
    
    total_batches = (len(pdf_files) - 1) // batch_size + 1
    
    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        print(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch)} files)")
        
        batch_results = []
        batch_failed = []
        
        for pdf_path in batch:
            try:
                result = chunk_pdf(pdf_path)
                if result:
                    batch_results.append(result)
                else:
                    batch_failed.append(pdf_path)
            except Exception as e:
                print(f"   ❌ Error processing {pdf_path}: {e}")
                batch_failed.append(pdf_path)
                continue
        
        all_results.extend(batch_results)
        failed_files.extend(batch_failed)
        
        print(f"   📊 Batch {batch_num} complete: {len(batch_results)} success, {len(batch_failed)} failed")
        
        # Save intermediate results
        if batch_num % 5 == 0:  # Every 5 batches
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            intermediate_file = f"intermediate_results_batch_{batch_num}_{timestamp}.json"
            with open(intermediate_file, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            print(f"   💾 Intermediate results saved to: {intermediate_file}")
    
    return all_results, failed_files

# Main processing
if __name__ == "__main__":
    # Find PDF files (start with smaller set for testing)
    pdf_files = glob.glob("*.pdf")  # Only root directory first
    pdf_files.extend(glob.glob("case_study/*.pdf"))  # Add case_study folder
    
    print(f"🔍 Found {len(pdf_files)} PDF files to process")
    
    if len(pdf_files) == 0:
        print("❌ No PDF files found!")
        exit()
    
    # Process PDFs
    results, failed = process_pdfs_batch(pdf_files, batch_size=10)
    
    # Save final results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"improved_pdf_chunks_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Save failed files
    failed_file = f"failed_pdfs_{timestamp}.txt"
    with open(failed_file, 'w', encoding='utf-8') as f:
        for pdf_file in failed:
            f.write(f"{pdf_file}\n")
    
    print(f"\n✅ Results saved to: {output_file}")
    print(f"❌ Failed files saved to: {failed_file}")
    
    # Summary
    total_chunks = sum(result['chunks_count'] for result in results)
    total_text = sum(result['text_length'] for result in results)
    
    print(f"\n📊 Final Summary:")
    print(f"   • PDFs processed: {len(results)}")
    print(f"   • PDFs failed: {len(failed)}")
    print(f"   • Total chunks: {total_chunks:,}")
    print(f"   • Total text: {total_text:,} characters")
    print(f"   • Success rate: {len(results)/(len(results)+len(failed))*100:.1f}%")
    
    print(f"\n🎉 Improved PDF chunking completed!")
