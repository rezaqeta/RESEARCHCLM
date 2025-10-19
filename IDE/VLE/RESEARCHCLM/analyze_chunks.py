import json
from pathlib import Path
from collections import defaultdict

docs_path = Path("artifacts/simple_store/documents.jsonl")

print("=" * 80)
print("📊 گزارش کامل PDF‌های پردازش‌شده و چانک‌ها")
print("=" * 80)

# Count total PDFs
case_study_dir = Path("case_study")
other_sources_dir = Path("other_sources")

total_case_pdfs = len(list(case_study_dir.glob("*.pdf"))) if case_study_dir.exists() else 0
total_other_pdfs = len(list(other_sources_dir.glob("*.pdf"))) if other_sources_dir.exists() else 0
total_all_pdfs = total_case_pdfs + total_other_pdfs

print(f"\n📁 تعداد کل PDF‌ها در دیسک:")
print(f"   🗂️  Case Study: {total_case_pdfs} فایل")
print(f"   🗂️  Other Sources: {total_other_pdfs} فایل")
print(f"   📊 مجموع کل: {total_all_pdfs} فایل PDF")

# Analyze documents.jsonl
file_chunks = defaultdict(int)
file_folder = {}

with open(docs_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            source = data.get('metadata', {}).get('source', 'unknown')
            file_chunks[source] += 1
            
            # Determine folder
            if 'case_study' in source:
                file_folder[source] = 'case_study'
            elif 'other_sources' in source:
                file_folder[source] = 'other_sources'
            else:
                file_folder[source] = 'unknown'
        except:
            pass

# Group by folder
case_study_files = {k: v for k, v in file_chunks.items() if file_folder.get(k) == 'case_study'}
other_sources_files = {k: v for k, v in file_chunks.items() if file_folder.get(k) == 'other_sources'}

case_study_chunks = sum(case_study_files.values())
other_sources_chunks = sum(other_sources_files.values())
total_chunks = sum(file_chunks.values())

print(f"\n✅ PDF‌های پردازش‌شده (چانک شده):")
print(f"   📄 مجموع فایل‌های پردازش‌شده: {len(file_chunks)} فایل")
print(f"\n   📂 Case Study:")
print(f"      ✓ فایل‌های پردازش‌شده: {len(case_study_files)} از {total_case_pdfs}")
print(f"      ✓ مجموع چانک‌ها: {case_study_chunks:,}")
print(f"\n   📂 Other Sources:")
print(f"      ✓ فایل‌های پردازش‌شده: {len(other_sources_files)} از {total_other_pdfs}")
print(f"      ✓ مجموع چانک‌ها: {other_sources_chunks:,}")

print(f"\n   📊 مجموع کل چانک‌ها: {total_chunks:,}")

# Calculate percentage
processed_count = len(file_chunks)
if total_all_pdfs > 0:
    percentage = (processed_count / total_all_pdfs) * 100
    print(f"\n📈 درصد پردازش‌شده: {percentage:.1f}% ({processed_count}/{total_all_pdfs})")

# Show remaining
remaining = total_all_pdfs - processed_count
if remaining > 0:
    print(f"\n⚠️  باقی‌مانده برای پردازش: {remaining:,} فایل PDF")
    print(f"   🗂️  Case Study: {total_case_pdfs - len(case_study_files)} فایل")
    print(f"   🗂️  Other Sources: {total_other_pdfs - len(other_sources_files)} فایل")
else:
    print(f"\n🎉 همه PDF‌ها پردازش شده‌اند! ✅")

# List processed files
print(f"\n📋 لیست فایل‌های Case Study پردازش‌شده:")
for i, (file, chunks) in enumerate(sorted(case_study_files.items()), 1):
    file_name = Path(file).name[:60] + "..." if len(Path(file).name) > 60 else Path(file).name
    print(f"   {i:2d}. {file_name:<65} ({chunks:,} چانک)")

print(f"\n📋 لیست فایل‌های Other Sources پردازش‌شده:")
for i, (file, chunks) in enumerate(sorted(other_sources_files.items()), 1):
    file_name = Path(file).name[:60] + "..." if len(Path(file).name) > 60 else Path(file).name
    print(f"   {i:2d}. {file_name:<65} ({chunks:,} چانک)")

# Top files by chunks
print(f"\n🔝 Top 5 فایل با بیشترین چانک:")
top_files = sorted(file_chunks.items(), key=lambda x: x[1], reverse=True)[:5]
for i, (file, chunks) in enumerate(top_files, 1):
    file_name = Path(file).name[:60]
    print(f"   {i}. {file_name}: {chunks:,} چانک")

print("\n" + "=" * 80)

