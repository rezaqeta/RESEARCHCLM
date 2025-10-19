# جدول وضعیت سیستم جست‌وجوی PDF

## ✅ موارد آماده برای استفاده

| مورد | وضعیت | نحوه اجرا | زمان اجرا | نیازمندی‌ها |
|------|--------|----------|-----------|-------------|
| **UI وب** | 🟢 فعال | `python scripts/ui_server.py` سپس `http://127.0.0.1:5055` | لحظه‌ای | Flask نصب باشد |
| **جست‌وجوی BM25** | 🟢 آماده | `python scripts/query_bm25.py -q "..." -k 10` | < 1 ثانیه | فقط داده‌های ingest شده |
| **جست‌وجوی TF-IDF** | 🟢 آماده | `python scripts/query_tfidf.py -q "..." -k 10` | 1-2 ثانیه | scikit-learn |
| **لینک مستقیم PDF** | 🟢 کار می‌کند | در UI روی نتیجه کلیک کنید | لحظه‌ای | مرورگر |
| **تکه‌بندی جمله‌ای** | 🟢 فعال | بخشی از ingestion | - | - |
| **فیلتر پوشه** | 🟢 فعال | در UI یا `--folder all/case_study/other_sources` | لحظه‌ای | - |

## 📊 آمار داده‌های فعلی

| آیتم | مقدار |
|------|-------|
| تعداد کل چانک‌ها | **2,592** |
| تعداد PDF ایندکس شده | **10** (5 case_study + 5 other_sources) |
| تعداد کل PDFهای موجود | **762** (21 case_study + 741 other_sources) |
| نوع تکه‌بندی | جمله‌ای (1 جمله per chunk) |
| حجم فایل داده | ~500 KB (documents.jsonl) |

## 🔜 موارد در انتظار تنظیمات

| مورد | وضعیت | نیازمندی | زمان تخمینی | هزینه |
|------|--------|----------|-------------|--------|
| **Embeddings محلی (sbert)** | 🟡 نیاز به venv | نصب sentence-transformers در venv تمیز | 5-10 دقیقه اولیه + 30-60 دقیقه برای encode کل corpus | CPU زیاد، دیسک ~300-500 MB |
| **Chroma Vector DB** | 🟡 محیط ناسازگار | حل conflict NumPy/ONNX | 5 دقیقه | دیسک ~500 MB-1 GB |
| **OpenRouter Embeddings** | 🟡 نیاز به شبکه | OPENROUTER_API_KEY + دسترسی پایدار | لحظه‌ای (per query) | هزینه API: ~$0.001 per 1K tokens |
| **خلاصه‌سازی OpenRouter** | 🟡 آماده اما غیرفعال | OPENROUTER_API_KEY | 2-5 ثانیه per query | هزینه API: ~$0.15 per 1M tokens (gpt-3.5-turbo) |
| **OCR برای PDF اسکن** | 🟡 پیشنهادی | Tesseract/OCRmyPDF | 1-5 دقیقه per PDF | CPU سنگین |

## 🎯 دستورات کاربردی

### اجرای UI

```powershell
cd R:\IDE\VLE\RESEARCHCLM
python scripts/ui_server.py
# سپس مرورگر: http://127.0.0.1:5055
```

### جست‌وجوی سریع از خط فرمان

```powershell
# BM25 (سریع‌ترین)
python scripts/query_bm25.py -q "behavioral nudge" -k 5

# TF-IDF (بهتر برای معنایی)
python scripts/query_tfidf.py -q "water conservation strategies" -k 10

# فقط case_study
python scripts/query_bm25.py -q "energy" --folder case_study -k 5
```

### افزودن PDFهای بیشتر

```powershell
# همه PDFها (زمان‌بر!)
python scripts/desk_ingest.py --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1

# 10 فایل نمونه از هر پوشه
python scripts/desk_ingest.py --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1 --limit-files-per-folder 10

# بازسازی کامل
python scripts/desk_ingest.py --recreate --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1
```

## 📈 مثال‌های نتایج واقعی

### Query: "behavioral interventions water conservation"
```
نتیجه 1: [other_sources] ...Sustainability_and_Climate_Change_Education.pdf | page 32 | score 9.18
نتیجه 2: [other_sources] ...Sustainability_and_Climate_Change_Education.pdf | page 30 | score 8.95
نتیجه 3: [other_sources] ...Sustainability_and_Climate_Change_Education.pdf | page 20 | score 8.34
نتیجه 4: [case_study] ...Energy-Use-Social-Comparisons.pdf | page 0 | score 8.31
نتیجه 5: [case_study] ...Watershed-Health-Scores.pdf | page 11 | score 7.82
```

## 🚀 مراحل بعدی پیشنهادی

### فاز 1: استفاده فعلی (همین حالا!)
1. UI را اجرا کنید: `python scripts/ui_server.py`
2. به http://127.0.0.1:5055 بروید
3. چند جست‌وجوی مختلف تست کنید
4. روی نتایج کلیک کنید و PDFها را ببینید

### فاز 2: افزایش داده (30-60 دقیقه)
1. همه PDFها را ingest کنید
2. تعداد چانک‌ها به ~100K-200K می‌رسد
3. پوشش کامل corpus

### فاز 3: Embeddings (1-2 ساعت)
1. venv تمیز بسازید
2. sentence-transformers نصب کنید
3. embeddings بسازید
4. جست‌وجوی معنایی فعال شود

### فاز 4: بهینه‌سازی (اختیاری)
1. Chroma فعال کنید (جست‌وجوی سریع‌تر)
2. OCR برای PDFهای اسکن
3. خلاصه‌سازی با LLM

## 🎓 نکات استفاده

### بهترین حالت جست‌وجو
- **سوالات کلی**: از BM25 استفاده کنید (سریع)
- **مفاهیم معنایی**: از TF-IDF استفاده کنید
- **پیدا کردن واژگان دقیق**: از BM25 با exact match
- **جست‌وجوی فارسی**: هر دو روش خوب کار می‌کنند

### تعداد نتایج مناسب
- **مرور سریع**: k=5
- **تحقیق دقیق**: k=10-20
- **استخراج جامع**: k=50+

### فیلترینگ هوشمند
- اگر دنبال case study هستید: `--folder case_study`
- اگر دنبال مقالات/گزارش‌ها: `--folder other_sources`
- برای پوشش کامل: `--folder all`

## 📞 پشتیبانی

اگر مشکلی پیش آمد:
1. بررسی کنید UI در حال اجراست: `curl http://127.0.0.1:5055`
2. log های terminal را بررسی کنید
