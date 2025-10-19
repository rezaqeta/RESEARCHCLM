Desk Research Pipeline (Case Studies + Other Sources)

Overview
- Ingest PDFs from `case_study` and `other_sources`.
- Split into chunks and embed via either local Sentence-Transformers or OpenRouter.
- Persist vectors in a simple local store (NumPy + JSONL) or Chroma (optional).
- Optional summarization via OpenRouter.

Prereqs
- Python 3.11+
- Packages: langchain, langchain-community, pypdf, requests
  - Optional (local embeddings): sentence-transformers
  - Optional (chroma backend): chromadb

Quick Start (Simple Store)
1) Ingest a tiny subset (smoke test)

```powershell
   # Uses OpenRouter embeddings by default when sbert fails
   $env:OPENROUTER_API_KEY = "sk-or-..."
   python scripts/desk_ingest.py --limit-files-per-folder 1 --recreate --store-backend simple --embed-backend openrouter --openrouter-model openai/text-embedding-3-small
```

2) Query the simple store

```powershell
   $env:OPENROUTER_API_KEY = "sk-or-..."
   python scripts/query_simple_store.py -q "urban water conservation behavioral interventions" --folder case_study -k 5
```

Optional: Chroma Backend
- If your environment supports Chromadb import (no NumPy/ONNX conflicts):

```powershell
   python scripts/desk_ingest.py --limit-files-per-folder 1 --recreate --store-backend chroma --embed-backend sbert --model sentence-transformers/all-MiniLM-L6-v2
   python scripts/query_vectorstore.py -q "urban water conservation behavioral interventions" --folder case_study -k 5
```

Summarization via OpenRouter

```powershell
$env:OPENROUTER_API_KEY = "sk-or-..."
python scripts/summarize_openrouter.py -q "urban water conservation behavioral interventions" --folder case_study -k 6
```

CLI Details
- `scripts/desk_ingest.py`
  - `--data-root` (default: r:/IDE/VLE/RESEARCHCLM)
  - `--folders` (default: case_study other_sources)
  - `--model` (sbert model name, default: sentence-transformers/paraphrase-multilingual-mpnet-base-v2)
  - `--chunk-size`/`--chunk-overlap` (default: 900/150)
  - `--batch-size` (default: 64)
  - `--limit-files-per-folder` (default: None)
  - `--store-backend` (simple | chroma)
  - `--collection`, `--chroma-path`, `--recreate` (when using chroma)
  - `--embed-backend` (sbert | openrouter)
  - `--openrouter-model` (e.g., openai/text-embedding-3-small)

- `scripts/query_simple_store.py`
  - `-q/--query`, `-k`, `--folder` (filter by source_folder)
  - `--store` (default: artifacts/simple_store)
  - `--embed-model` (OpenRouter embedding model; reads OPENROUTER_API_KEY)

- `scripts/query_vectorstore.py`
  - `--chroma-path`, `--collection`
  - `-q/--query`, `-k`, `--folder`

Notes
- For bilingual Farsi/English corpora, prefer `paraphrase-multilingual-mpnet-base-v2` when using local sbert.
- If Chromadb import fails due to NumPy/ONNX runtime, use the Simple Store path.
- You can filter queries by `source_folder` to separate case studies from other sources.