# 🚀 شروع سریع - UI جست‌وجوی PDF

## ✅ الان چی آماده است؟

| آیتم | وضعیت |
|------|-------|
| UI وب | ✅ اجرا شده روی http://127.0.0.1:5055 |
| تعداد PDF | ✅ 10 فایل ایندکس شده |
| تعداد چانک | ✅ 2,592 قطعه متن |
| جست‌وجو | ✅ BM25 + TF-IDF |
| لینک PDF | ✅ کلیک کنید → PDF باز می‌شود |

---

## 🎯 همین حالا امتحان کنید!

### گام 1: مرورگر را باز کنید
```
http://127.0.0.1:5055
```

### گام 2: جست‌وجو کنید
مثال‌ها:
- `behavioral interventions water`
- `energy nudge consumption`
- `climate change policy`
- `رفتار محیط زیستی`

### گام 3: نتایج را ببینید
- روی هر نتیجه کلیک کنید
- PDF در صفحه مربوطه باز می‌شود

---

## 📊 نمونه نتایج

**جست‌وجو:** "behavioral interventions water conservation"

```
✓ نتیجه 1: Sustainability and Climate Change Education.pdf
  صفحه 32 | امتیاز: 9.18 | پوشه: other_sources
  
✓ نتیجه 2: Energy Use Social Comparisons.pdf  
  صفحه 0 | امتیاز: 8.31 | پوشه: case_study
```

---

## ⚡ دستورات مفید

### اگر UI بسته شد، دوباره اجرا کنید:

```powershell
cd R:\IDE\VLE\RESEARCHCLM
python scripts/ui_server.py
```

### جست‌وجو از خط فرمان (بدون UI):

```powershell
python scripts/query_bm25.py -q "your search" -k 10
```

### افزودن PDFهای بیشتر:

```powershell
# 10 فایل دیگر
python scripts/desk_ingest.py --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1 --limit-files-per-folder 10

# همه فایل‌ها (زمان‌بر!)  
python scripts/desk_ingest.py --store-backend simple --no-embed --loader pdfplumber --split-mode sentence --sentences-per-chunk 1
```

---

## 📁 فایل‌های مهم

| فایل | توضیح |
|------|-------|
| `UI_USAGE_GUIDE.md` | راهنمای کامل UI |
| `STATUS_TABLE.md` | جدول وضعیت کامل سیستم |
| `README_DESK_RESEARCH.md` | راهنمای جامع |
| `scripts/ui_server.py` | سرور UI |
| `artifacts/simple_store/` | داده‌های ایندکس شده |

---

## 🎉 تبریک!

سیستم شما آماده است. می‌توانید:
- ✅ در 10 PDF جست‌وجو کنید
- ✅ نتایج را با امتیاز مرتبط ببینید  
- ✅ مستقیماً به صفحه PDF بروید
- ✅ با فیلترهای مختلف جست‌وجو کنید

**سوال دارید؟** `UI_USAGE_GUIDE.md` یا `STATUS_TABLE.md` را باز کنید.

---

**نکته:** برای افزودن همه 762 فایل، دستور ingest را بدون `--limit-files-per-folder` اجرا کنید. ممکن است 30-60 دقیقه طول بکشد.



