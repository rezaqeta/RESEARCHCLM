import json
from pathlib import Path
from collections import defaultdict

# Paths
index_path = Path("r:/IDE/VLE/RESEARCHCLM/artifacts/simple_store/index.json")
case_study_dir = Path("r:/IDE/VLE/RESEARCHCLM/case_study")
other_sources_dir = Path("r:/IDE/VLE/RESEARCHCLM/other_sources")

print("=" * 70)
print("📊 گزارش کامل وضعیت PDFها")
print("=" * 70)

# Count total PDFs
case_study_pdfs = list(case_study_dir.glob("*.pdf")) if case_study_dir.exists() else []
other_sources_pdfs = list(other_sources_dir.glob("*.pdf")) if other_sources_dir.exists() else []

total_pdfs = len(case_study_pdfs) + len(other_sources_pdfs)

print(f"\n📁 تعداد کل PDF‌ها در فولدرها:")
print(f"   🗂️  Case Study: {len(case_study_pdfs)} فایل")
print(f"   🗂️  Other Sources: {len(other_sources_pdfs)} فایل")
print(f"   📊 مجموع: {total_pdfs} فایل PDF")

# Read index to see processed files
if index_path.exists():
    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    file_stats = index_data.get('file_stats', [])
    
    print(f"\n✅ PDF‌های پردازش‌شده (چانک شده):")
    print(f"   📄 تعداد: {len(file_stats)} فایل")
    
    # Group by folder
    by_folder = defaultdict(list)
    total_chunks = 0
    
    for file_info in file_stats:
        file_name = Path(file_info['file']).name
        folder = file_info.get('folder', 'unknown')
        chunks = file_info.get('chunks', 0)
        total_chunks += chunks
        
        by_folder[folder].append({
            'name': file_name,
            'chunks': chunks
        })
    
    for folder, files in by_folder.items():
        folder_name = "Case Study" if "case_study" in folder else "Other Sources"
        total_folder_chunks = sum(f['chunks'] for f in files)
        print(f"\n   📂 {folder_name}:")
        print(f"      ✓ فایل‌های پردازش‌شده: {len(files)}")
        print(f"      ✓ مجموع چانک‌ها: {total_folder_chunks:,}")
    
    print(f"\n   📊 مجموع کل چانک‌ها: {total_chunks:,}")
    
    # Calculate percentage
    processed_count = len(file_stats)
    if total_pdfs > 0:
        percentage = (processed_count / total_pdfs) * 100
        print(f"\n📈 درصد پردازش‌شده: {percentage:.1f}% ({processed_count}/{total_pdfs})")
    
    # Show unprocessed
    unprocessed = total_pdfs - processed_count
    if unprocessed > 0:
        print(f"\n⚠️  PDF‌های پردازش نشده: {unprocessed} فایل")
        print(f"   💡 برای پردازش همه: python scripts/desk_ingest.py --recreate --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1")
    else:
        print(f"\n🎉 همه PDF‌ها پردازش شده‌اند! ✅")
    
    # Show sample files
    if file_stats:
        print(f"\n📋 نمونه فایل‌های پردازش‌شده (5 تا اول):")
        for i, file_info in enumerate(file_stats[:5], 1):
            file_name = Path(file_info['file']).name
            chunks = file_info.get('chunks', 0)
            print(f"   {i}. {file_name}: {chunks} چانک")
        
        if len(file_stats) > 5:
            print(f"   ... و {len(file_stats) - 5} فایل دیگر")

else:
    print(f"\n❌ فایل index.json یافت نشد!")
    print(f"   هیچ PDF ای پردازش نشده است.")

print("\n" + "=" * 70)

