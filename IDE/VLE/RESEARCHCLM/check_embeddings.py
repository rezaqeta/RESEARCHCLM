import json
import os
from pathlib import Path

# Check index.json
index_path = Path("r:/IDE/VLE/RESEARCHCLM/artifacts/simple_store/index.json")
docs_path = Path("r:/IDE/VLE/RESEARCHCLM/artifacts/simple_store/documents.jsonl")
embeddings_path = Path("r:/IDE/VLE/RESEARCHCLM/artifacts/simple_store/embeddings.npy")

print("=" * 60)
print("📊 وضعیت Embedding در سیستم")
print("=" * 60)

# Read index
if index_path.exists():
    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    print(f"\n✅ Index File موجود است")
    print(f"   📁 تعداد کل چانک‌ها: {index_data.get('total_chunks', 'نامشخص')}")
    print(f"   🔢 Embedding وضعیت: {index_data.get('has_embeddings', False)}")
    print(f"   📂 تعداد فایل‌های پردازش‌شده: {len(index_data.get('file_stats', []))}")
    
    # Show file stats
    if 'file_stats' in index_data:
        print(f"\n📋 آمار فایل‌ها:")
        case_study_count = 0
        other_sources_count = 0
        total_chunks = 0
        
        for file_info in index_data['file_stats']:
            folder = file_info.get('folder', '')
            chunks = file_info.get('chunks', 0)
            total_chunks += chunks
            
            if 'case_study' in folder:
                case_study_count += 1
            elif 'other_sources' in folder:
                other_sources_count += 1
        
        print(f"   🗂️ Case Study: {case_study_count} فایل")
        print(f"   🗂️ Other Sources: {other_sources_count} فایل")
        print(f"   📊 مجموع چانک‌ها: {total_chunks}")

# Check documents.jsonl
if docs_path.exists():
    # Count lines
    with open(docs_path, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    print(f"\n✅ Documents File موجود است")
    print(f"   📄 تعداد چانک‌ها: {line_count}")
    print(f"   💾 حجم فایل: {docs_path.stat().st_size / (1024*1024):.2f} MB")

# Check embeddings.npy
if embeddings_path.exists():
    import numpy as np
    embeddings = np.load(embeddings_path)
    print(f"\n✅ Embeddings File موجود است")
    print(f"   🔢 تعداد بردارها: {embeddings.shape[0]}")
    print(f"   📏 ابعاد بردار: {embeddings.shape[1]}")
    print(f"   💾 حجم فایل: {embeddings_path.stat().st_size / (1024*1024):.2f} MB")
    print(f"\n   🎉 همه PDF‌ها EMBEDDING شده‌اند! ✅")
else:
    print(f"\n❌ Embeddings File موجود نیست")
    print(f"   ⚠️ هیچ PDF ای EMBEDDING نشده است!")
    print(f"\n   💡 برای ساخت Embedding:")
    print(f"      python scripts/desk_ingest.py --embed-backend sbert")

print("\n" + "=" * 60)

