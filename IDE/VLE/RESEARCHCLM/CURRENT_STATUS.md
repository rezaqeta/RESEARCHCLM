# 🎯 وضعیت فعلی سیستم جست‌وجوی PDF

**آخرین به‌روزرسانی:** 16 اکتبر 2025

---

## 🆕 نصب جدید: LlamaIndex (16 اکتبر 2025)

### ✅ LlamaIndex v0.14.5 نصب شد!
```
📍 محل نصب: r:\IDE\VLE\RESEARCHCLM\llamaindex_env\
🔧 قابلیت‌ها: Document Loading, Text Chunking, Semantic Search
🌐 بدون نیاز به API Key (استفاده از مدل‌های محلی)
```

### 📚 فایل‌های ایجاد شده:
```
✅ LLAMAINDEX_GUIDE.md                    # راهنمای کامل (12 بخش)
✅ LLAMAINDEX_QUICKSTART.md               # شروع سریع
✅ LLAMAINDEX_INSTALLATION_SUMMARY.md     # خلاصه نصب
✅ llamaindex_pdf_chunker.py              # اسکریپت تکه‌بندی PDF
✅ llamaindex_local_search.py             # جست‌وجوی معنایی محلی
✅ llamaindex_research_pipeline.py        # پایپلاین کامل تحقیق
✅ activate_llamaindex.ps1                # اسکریپت فعال‌سازی
✅ requirements_llamaindex.txt            # وابستگی‌ها
```

### 🚀 راه‌اندازی سریع:

```powershell
# روش 1: استفاده از اسکریپت
.\activate_llamaindex.ps1

# روش 2: دستی
.\llamaindex_env\Scripts\Activate.ps1

# اجرای مثال‌ها:
python llamaindex_pdf_chunker.py           # تکه‌بندی PDF
python llamaindex_local_search.py          # جست‌وجوی محلی
python llamaindex_research_pipeline.py     # پایپلاین کامل
```

---

## ✅ آماده و فعال

### 📊 آمار سیستم:
```
📁 تعداد PDF: 20 فایل
📄 تعداد چانک: 19,530 قطعه متن
🗂️ Case Study: 3,223 چانک (6 فایل)
🗂️ Other Sources: 16,307 چانک (14 فایل)
```

### 🖥️ UI وب:
```
🌐 آدرس: http://127.0.0.1:5055
✅ وضعیت: فعال و در حال اجرا
🔍 قابلیت‌ها: جست‌وجوی BM25، TF-IDF، لینک مستقیم به PDF
```

---

## 🔥 نمونه نتایج واقعی

### Query 1: "behavioral interventions nudge energy"
```
نتیجه 1: World_Bank_Behavioral_Science.pdf
  • امتیاز: 9.75
  • صفحه: 94
  • متن: "Many projects involving behavioral interventions..."

نتیجه 2: Climate_Change_Interventions.pdf
  • امتیاز: 9.48
  • صفحه: 28
  • متن: "behavioral interventions using qualitative..."
```

### Query 2: "water conservation policy"
```
نتیجه 1: Behavioral_Science_Climate_Change.pdf
  • امتیاز: 11.17 ⭐
  • صفحه: 47
  • متن: "Conservation agriculture: Concepts..."

نتیجه 2: Water_Agreements_Ecuador.pdf
  • امتیاز: 9.48
  • صفحه: 40
  • متن: "social proof for water conservation..."
```

---

## 🚀 دستورات کاربردی

### راه‌اندازی UI:

```powershell
cd R:\IDE\VLE\RESEARCHCLM
python scripts/ui_server.py
```

سپس مرورگر: http://127.0.0.1:5055

### جست‌وجوی CLI (بدون UI):

```powershell
# BM25 (سریع):
python scripts/query_bm25.py -q "your query" -k 10

# TF-IDF (معنایی‌تر):
python scripts/query_tfidf.py -q "your query" -k 10

# فقط Case Studies:
python scripts/query_bm25.py -q "energy" --folder case_study -k 5

# فقط Other Sources:
python scripts/query_bm25.py -q "policy" --folder other_sources -k 10
```

### افزودن PDFهای بیشتر:

```powershell
# 10 فایل دیگر:
python scripts/desk_ingest.py --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1 --limit-files-per-folder 25

# 20 فایل دیگر:
python scripts/desk_ingest.py --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1 --limit-files-per-folder 35

# همه فایل‌ها (زمان‌بر: 30-60 دقیقه):
python scripts/desk_ingest.py --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1
```

---

## 📈 مقایسه قبل و بعد

| مورد | قبل | بعد | بهبود |
|------|-----|-----|-------|
| تعداد PDF | 10 | **20** | 2x |
| تعداد چانک | 2,592 | **19,530** | 7.5x |
| امتیاز نتایج | 0-8 | **9-11** | بهتر |
| کیفیت نتایج | متوسط | **عالی** | ✅ |

---

## 🎯 مثال‌های کاربردی

### 1. پیدا کردن مداخلات رفتاری برای انرژی:
```
UI → جست‌وجو: "behavioral interventions energy consumption"
فیلتر: all
نتیجه: 5 نتیجه با امتیاز 8.6-9.7
```

### 2. جست‌وجوی Case Study خاص:
```
UI → جست‌وجو: "social comparison nudge"
فیلتر: case_study
نتیجه: مطالعات Opower و مشابه
```

### 3. تحقیق در سیاست‌های آب:
```
CLI → python scripts/query_bm25.py -q "water policy conservation" -k 10
نتیجه: گزارش‌های World Bank، مطالعات Ecuador و...
```

---

## 🔮 مراحل بعدی (اختیاری)

### فاز بعدی: افزایش داده
- [ ] افزودن 30-50 PDF دیگر (10-20 دقیقه)
- [ ] تست با queries مختلف
- [ ] بررسی کیفیت نتایج

### فاز پیشرفته: Embeddings
- [ ] ساخت venv تمیز
- [ ] نصب sentence-transformers
- [ ] ایجاد embeddings عصبی
- [ ] جست‌وجوی معنایی کامل

### فاز نهایی: بهینه‌سازی
- [ ] Chroma vector database
- [ ] OCR برای PDFهای اسکن
- [ ] خلاصه‌سازی با LLM

---

## 📞 فایل‌های مرجع

| فایل | توضیح |
|------|-------|
| `QUICK_START_UI.md` | راهنمای شروع سریع |
| `UI_USAGE_GUIDE.md` | راهنمای کامل UI |
| `STATUS_TABLE.md` | جدول وضعیت کامل |
| `README_DESK_RESEARCH.md` | راهنمای جامع تکنیکال |
| `LLAMAINDEX_QUICKSTART.md` | **جدید:** شروع سریع LlamaIndex |
| `LLAMAINDEX_GUIDE.md` | **جدید:** راهنمای کامل LlamaIndex |
| `LLAMAINDEX_INSTALLATION_SUMMARY.md` | **جدید:** خلاصه نصب LlamaIndex |

---

## ✨ نکات مهم

1. **UI در پس‌زمینه اجرا نمی‌شود**: باید در یک PowerShell جدا اجرا شود
2. **بعضی PDFها خراب هستند**: خطاهای "No /Root object" عادی است
3. **امتیازهای بالا = مرتبط‌تر**: امتیاز > 9 معمولاً خیلی مرتبط است
4. **TF-IDF بهتر از BM25**: برای queries معنایی از TF-IDF استفاده کنید

---