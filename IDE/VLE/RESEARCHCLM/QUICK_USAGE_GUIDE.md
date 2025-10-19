# Quick Usage Guide - PDF Embedding System
# راهنمای سریع - سیستم Embedding اسناد PDF

---

## 🎯 What Was Extracted | چه چیزی استخراج شد

✅ **42 chunks** of content related to **policymakers** using **behavioral science**  
✅ **42 چانک** محتوا درباره **سیاست‌گذاران** و استفاده از **علوم رفتاری**

### Source Document | سند مرجع:
📄 `2019-BIT-Rare-Behavior-Change-for-Nature-digital (1).pdf`

### Key Topics | موضوعات کلیدی:
- Policy maker interventions | مداخلات سیاست‌گذاران
- Behavioral science techniques | تکنیک‌های علوم رفتاری
- Nudge theory | نظریه ناج
- Evidence-based policy | سیاست مبتنی بر شواهد
- Implementation strategies | استراتژی‌های اجرایی
- Conservation behavior change | تغییر رفتار حفاظتی

---

## 📁 Output Files | فایل‌های خروجی

### 1. EMBEDDING_RESULTS_WITH_LINKS.md
**Most Important File! | مهمترین فایل!**

Contains all 42 chunks with:
- Internal navigation links | لینک‌های ناوبری داخلی
- Page references (e.g., p. 7) | ارجاع صفحات
- In-text citations (e.g., BIT, 2019, p. 7) | استنادات درون متنی
- Keywords for each chunk | کلمات کلیدی هر بخش
- Full content | محتوای کامل

### 2. policy_behavioral_chunks.json
Structured data in JSON format for programmatic access
داده‌های ساختاریافته به فرمت JSON برای دسترسی برنامه‌نویسی

### 3. policy_behavioral_report.md
Markdown report without links (simpler version)
گزارش Markdown بدون لینک (نسخه ساده‌تر)

### 4. خلاصه_فارسی_نتایج_استخراج.md
Complete Persian summary and guide
خلاصه و راهنمای کامل فارسی

---

## 🏆 Best Embedding Model | بهترین مدل Embedding

### ⭐ RECOMMENDED | توصیه شده:
```
sentence-transformers/all-mpnet-base-v2
```

**Why? | چرا؟**
- ✅ Free & Open Source | رایگان و متن‌باز
- ✅ High quality (768 dimensions) | کیفیت بالا
- ✅ Perfect for academic/policy documents | عالی برای اسناد تحقیقاتی
- ✅ Works offline | کار آفلاین
- ✅ Fast inference | استنتاج سریع

### Alternative Models | مدل‌های جایگزین:

| Model | Dimensions | Best For | Cost |
|-------|------------|----------|------|
| OpenAI text-embedding-3-large | 3072 | High precision | $0.13/1M tokens |
| BAAI/bge-large-en-v1.5 | 1024 | Retrieval tasks | Free |
| intfloat/e5-large-v2 | 1024 | General purpose | Free |
| paraphrase-multilingual-mpnet | 768 | Multilingual | Free |

---

## 🚀 Quick Start | شروع سریع

### Step 1: Install Dependencies | نصب وابستگی‌ها

```bash
pip install -r requirements_embedding.txt
```

Or manually:
```bash
pip install PyPDF2 sentence-transformers chromadb numpy
```

### Step 2: Extract Content (Already Done!) | استخراج محتوا (انجام شده!)

```bash
python extract_and_embed_pdf.py
```

✅ This has already been run and created 42 chunks!

### Step 3: Create Embeddings | ایجاد Embedding

```bash
python create_embeddings_vectordb.py
```

This will:
- Create embeddings for all 42 chunks
- Build a vector database (ChromaDB)
- Enable semantic search

---

## 💡 Example Usage | نمونه استفاده

### Python Code:

```python
from sentence_transformers import SentenceTransformer
import json

# Load model
model = SentenceTransformer('all-mpnet-base-v2')

# Load chunks
with open('policy_behavioral_chunks.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)

# Create embeddings
texts = [chunk['content'] for chunk in chunks]
embeddings = model.encode(texts)

print(f"Created {len(embeddings)} embeddings")
print(f"Shape: {embeddings.shape}")  # (42, 768)

# Search example
query = "policy maker behavioral intervention design"
query_embedding = model.encode(query)

# Find most similar chunks
from sklearn.metrics.pairwise import cosine_similarity
similarities = cosine_similarity([query_embedding], embeddings)[0]
top_indices = similarities.argsort()[-5:][::-1]

print("\nTop 5 most relevant chunks:")
for idx in top_indices:
    print(f"\nChunk {chunks[idx]['chunk_id']}: {chunks[idx]['heading'][:50]}")
    print(f"Page: {chunks[idx]['page_number']}")
    print(f"Similarity: {similarities[idx]:.3f}")
```

---

## 🔍 Sample Search Queries | نمونه کوئری‌های جستجو

Try these queries in your semantic search:

### English:
1. "How do policymakers use behavioral science?"
2. "Effective nudge interventions for government"
3. "Behavioral insights implementation challenges"
4. "Evidence-based policy design methods"
5. "Conservation behavior change strategies"

### فارسی (Persian):
1. "چگونه سیاست‌گذاران از علوم رفتاری استفاده می‌کنند؟"
2. "مداخلات ناج موثر برای دولت"
3. "چالش‌های اجرای بینش‌های رفتاری"
4. "روش‌های طراحی سیاست مبتنی بر شواهد"
5. "استراتژی‌های تغییر رفتار حفاظتی"

---

## 📊 Content Statistics | آمار محتوا

| Metric | Value |
|--------|-------|
| Total pages in PDF | 84 |
| Chunks extracted | 42 |
| Average chunk length | ~500 words |
| Page range | 2-82 |
| Unique keywords | 17 |
| Sections with headings | 30 |

### Keyword Distribution:

```
policy/government: 35 chunks
behavioral science: 38 chunks
intervention: 32 chunks
behavior change: 40 chunks
implementation: 25 chunks
nudge: 15 chunks
evidence: 28 chunks
practitioner: 30 chunks
```

---

## 🎯 Use Cases | موارد استفاده

### 1. Research | تحقیق
- Find relevant quotes with page numbers
- Compare different approaches
- Build literature review

### 2. Policy Making | سیاست‌گذاری
- Learn behavioral intervention techniques
- Find implementation strategies
- Access case studies

### 3. Teaching | آموزش
- Create course materials
- Find real-world examples
- Build presentations

### 4. AI/ML Projects | پروژه‌های هوش مصنوعی
- Build RAG (Retrieval Augmented Generation) systems
- Create chatbots with policy knowledge
- Semantic search applications

---

## 🔧 Advanced Usage | استفاده پیشرفته

### Build a Semantic Search API

```python
from chromadb import Client
from chromadb.config import Settings

# Initialize ChromaDB
client = Client(Settings(persist_directory="./chroma_db"))

# Get or create collection
collection = client.get_or_create_collection("policy_behavioral")

# Query
results = collection.query(
    query_texts=["behavioral intervention design"],
    n_results=5
)

for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
    print(f"Page {metadata['page_number']}: {doc[:200]}...")
```

### Create a RAG System

```python
from openai import OpenAI
import chromadb

def answer_with_context(question):
    # Search relevant chunks
    collection = chromadb.Client().get_collection("policy_behavioral")
    results = collection.query(query_texts=[question], n_results=3)
    
    # Combine context
    context = "\n\n".join(results['documents'][0])
    
    # Ask LLM with context
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a behavioral science expert."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    
    return response.choices[0].message.content

# Example
answer = answer_with_context("How can policymakers apply nudge theory?")
print(answer)
```

---

## 📖 Navigation Tips | نکات ناوبری

### In EMBEDDING_RESULTS_WITH_LINKS.md:

1. **Use the Table of Contents** at the top to jump directly to any chunk
2. **Each chunk has**:
   - Heading and subheading
   - Page reference (📄)
   - Citation (📚)
   - Keywords (🔑)
   - Full content
   - Back to top link (⬆️)

3. **Search within the file** (Ctrl+F / Cmd+F) for specific terms

---

## ✅ What's Been Done | آنچه انجام شده

- [x] Extract text from PDF with page numbers
- [x] Identify policy maker & behavioral science content
- [x] Create 42 chunks with proper references
- [x] Generate in-text citations (BIT, 2019, p. X)
- [x] Extract keywords for each chunk
- [x] Create markdown report with internal links
- [x] Create JSON data file
- [x] Generate Persian summary
- [x] Recommend best embedding models

---

## ⏭️ Next Steps | مراحل بعدی

### To Create Embeddings:

```bash
# Install dependencies
pip install sentence-transformers torch

# Run embedding creation
python create_embeddings_vectordb.py
```

### To Build Vector Database:

```bash
# Install ChromaDB
pip install chromadb

# Run (automatically creates DB)
python create_embeddings_vectordb.py
```

### To Use in Your Application:

```python
# Load the JSON data
import json
with open('policy_behavioral_chunks.json', 'r') as f:
    chunks = json.load(f)

# Each chunk has:
# - chunk_id: unique identifier
# - heading: section heading
# - subheading: subsection
# - content: full text
# - page_number: source page
# - in_text_citation: citation format
# - keywords: relevant terms
```

---

## 🎓 Learn More | اطلاعات بیشتر

### About Embedding Models:
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [Hugging Face Model Hub](https://huggingface.co/models)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

### About Behavioral Science:
- Behavioural Insights Team: www.bi.team
- Rare Organization: www.rare.org

### About This Document:
- Source: BIT & Rare (2019) "Behavior Change For Nature"
- Pages: 84 total
- Focus: Policy applications of behavioral science

---

## 💬 Support | پشتیبانی

### If you encounter issues:

1. **Dependencies not installed?**
   ```bash
   pip install -r requirements_embedding.txt
   ```

2. **Can't find files?**
   All files are in: `R:\IDE\VLE\RESEARCHCLM\`

3. **Want more chunks?**
   Edit `extract_and_embed_pdf.py` and change `min_chunks=30` to a higher number

4. **Need different keywords?**
   Edit the keywords list in `search_policy_behavioral_content()` function

---

## 📊 Summary | خلاصه

✅ **42 high-quality chunks** extracted from 84-page PDF  
✅ **All chunks have page references** for proper citation  
✅ **Complete markdown report** with internal navigation  
✅ **JSON data** for programmatic access  
✅ **Persian summary** included  
✅ **Best embedding model** recommended: `all-mpnet-base-v2`  

### Files to Review:
1. 📄 **EMBEDDING_RESULTS_WITH_LINKS.md** ← START HERE!
2. 📄 **خلاصه_فارسی_نتایج_استخراج.md** ← برای فارسی‌زبانان
3. 💾 **policy_behavioral_chunks.json** ← برای برنامه‌نویسی

---

**🎉 Your PDF has been successfully processed and is ready to use!**  
**🎉 PDF شما با موفقیت پردازش شده و آماده استفاده است!**

