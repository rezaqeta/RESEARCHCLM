"""
Analyze PDF Chunking Results - Find Failed PDFs
"""

import os
import glob
import json
from datetime import datetime

print("="*70)
print("📊 PDF Chunking Analysis - Failed Files")
print("="*70)

# Find all PDF files
all_pdf_files = glob.glob("**/*.pdf", recursive=True)
print(f"🔍 Total PDF files found: {len(all_pdf_files)}")

# Find result files
result_files = glob.glob("pdf_chunks_results_*.json")
if not result_files:
    result_files = glob.glob("test_pdf_chunks_*.json")

if not result_files:
    print("❌ No result files found!")
    exit()

# Get the latest result file
latest_result = max(result_files, key=os.path.getctime)
print(f"📄 Using result file: {latest_result}")

# Load results
with open(latest_result, 'r', encoding='utf-8') as f:
    results = json.load(f)

# Get processed files
processed_files = {result['file_path'] for result in results}
print(f"✅ Successfully processed: {len(processed_files)} PDFs")

# Find failed files
failed_files = []
for pdf_file in all_pdf_files:
    if pdf_file not in processed_files:
        failed_files.append(pdf_file)

print(f"❌ Failed to process: {len(failed_files)} PDFs")

if failed_files:
    print(f"\n📋 Failed PDF Files List:")
    print("-" * 50)
    
    # Group by error type (based on common patterns)
    eof_errors = []
    invalid_arg_errors = []
    other_errors = []
    
    for pdf_file in failed_files:
        if "other_sources" in pdf_file:
            eof_errors.append(pdf_file)
        elif "case_study" in pdf_file:
            invalid_arg_errors.append(pdf_file)
        else:
            other_errors.append(pdf_file)
    
    if eof_errors:
        print(f"\n🔴 EOF Marker Errors ({len(eof_errors)} files):")
        for i, pdf_file in enumerate(eof_errors[:10], 1):  # Show first 10
            print(f"   {i:2d}. {os.path.basename(pdf_file)}")
        if len(eof_errors) > 10:
            print(f"   ... and {len(eof_errors) - 10} more")
    
    if invalid_arg_errors:
        print(f"\n🟡 Invalid Argument Errors ({len(invalid_arg_errors)} files):")
        for i, pdf_file in enumerate(invalid_arg_errors[:10], 1):
            print(f"   {i:2d}. {os.path.basename(pdf_file)}")
        if len(invalid_arg_errors) > 10:
            print(f"   ... and {len(invalid_arg_errors) - 10} more")
    
    if other_errors:
        print(f"\n🟠 Other Errors ({len(other_errors)} files):")
        for i, pdf_file in enumerate(other_errors[:10], 1):
            print(f"   {i:2d}. {os.path.basename(pdf_file)}")
        if len(other_errors) > 10:
            print(f"   ... and {len(other_errors) - 10} more")
    
    # Save failed files list
    failed_list_file = f"failed_pdfs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(failed_list_file, 'w', encoding='utf-8') as f:
        f.write("Failed PDF Files List\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total failed: {len(failed_files)}\n\n")
        
        f.write("EOF Marker Errors:\n")
        for pdf_file in eof_errors:
            f.write(f"{pdf_file}\n")
        
        f.write("\nInvalid Argument Errors:\n")
        for pdf_file in invalid_arg_errors:
            f.write(f"{pdf_file}\n")
        
        f.write("\nOther Errors:\n")
        for pdf_file in other_errors:
            f.write(f"{pdf_file}\n")
    
    print(f"\n💾 Failed files list saved to: {failed_list_file}")

# Summary statistics
total_chunks = sum(result['chunks_count'] for result in results)
total_text = sum(result['text_length'] for result in results)

print(f"\n📊 Summary Statistics:")
print(f"   • Total PDF files: {len(all_pdf_files)}")
print(f"   • Successfully processed: {len(processed_files)} ({len(processed_files)/len(all_pdf_files)*100:.1f}%)")
print(f"   • Failed to process: {len(failed_files)} ({len(failed_files)/len(all_pdf_files)*100:.1f}%)")
print(f"   • Total chunks created: {total_chunks:,}")
print(f"   • Total text extracted: {total_text:,} characters")

# Success rate
success_rate = len(processed_files) / len(all_pdf_files) * 100
print(f"\n🎯 Success Rate: {success_rate:.1f}%")

if success_rate >= 90:
    print("✅ Excellent success rate!")
elif success_rate >= 80:
    print("✅ Good success rate!")
elif success_rate >= 70:
    print("⚠️ Moderate success rate")
else:
    print("❌ Low success rate - needs improvement")

print(f"\n🔧 Recommendations:")
if eof_errors:
    print(f"   • {len(eof_errors)} files have EOF marker issues (likely corrupted)")
if invalid_arg_errors:
    print(f"   • {len(invalid_arg_errors)} files have path issues (special characters)")
print(f"   • Consider using alternative PDF readers for failed files")
print(f"   • Try pdfplumber or fitz (PyMuPDF) for better compatibility")
