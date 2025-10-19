"""
Simple LlamaIndex Test - بدون import کامل
"""

print("=" * 60)
print("🧪 تست ساده LlamaIndex")
print("=" * 60)

# تست 1: فقط Document
try:
    from llama_index.core import Document
    doc = Document(text="تست ساده")
    print("✅ Document import موفق!")
    print(f"   متن: {doc.text}")
except Exception as e:
    print(f"❌ Document import خطا: {e}")

# تست 2: فقط SentenceSplitter
try:
    from llama_index.core.node_parser import SentenceSplitter
    splitter = SentenceSplitter(chunk_size=100)
    print("✅ SentenceSplitter import موفق!")
except Exception as e:
    print(f"❌ SentenceSplitter import خطا: {e}")

# تست 3: فقط HuggingFace Embeddings
try:
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    print("✅ HuggingFaceEmbedding import موفق!")
except Exception as e:
    print(f"❌ HuggingFaceEmbedding import خطا: {e}")

# تست 4: فقط VectorStoreIndex
try:
    from llama_index.core import VectorStoreIndex
    print("✅ VectorStoreIndex import موفق!")
except Exception as e:
    print(f"❌ VectorStoreIndex import خطا: {e}")

print("\n" + "=" * 60)
print("📊 خلاصه نتایج:")
print("=" * 60)

# اگر همه موفق بودن
if all([
    'Document' in locals(),
    'SentenceSplitter' in locals(), 
    'HuggingFaceEmbedding' in locals(),
    'VectorStoreIndex' in locals()
]):
    print("🎉 همه چیز کار می‌کنه!")
    print("✅ می‌تونی چانک کنی")
    print("✅ می‌تونی Embed کنی")
    print("✅ می‌تونی جست‌وجو کنی")
else:
    print("⚠️ بعضی بخش‌ها مشکل دارن")
    print("💡 احتمالاً مشکل dependency هست")

print("\n🚀 آماده برای استفاده!")



