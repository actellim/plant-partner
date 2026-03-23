# Data Acquisition & Extraction Process

This document outlines the engineering steps taken to acquire, normalize, and merge the plant characteristic datasets for the Plant Partner project.

## 1. USDA PLANTS Database (Native/North American)
- **Source:** [USDA PLANTS Database Characteristic API](https://plants.sc.egov.usda.gov/home/charSearch).
- **Acquisition Strategy:** 
  - A master symbol list (`plantlst.txt`) acquired from the [USDA website](https://plants.sc.egov.usda.gov/downloads) was used to iterate through the undocumented internal USDA JSON API.
  - A custom scraper (`src/usda_scraper.js`) was developed with robust rate limiting (500ms delay) and exponential backoff retries to ensure a complete and reliable extraction.
  - **Artifact:** `usda_data.jsonl` (scraped line-by-line to allow for resumability).
- **License:** Public Domain (US Government Data).

## 2. Plants For A Future (PFAF) (Garden/Edible)
- **Source:** [Plants For A Future](https://pfaf.org/) (via saulshanabrook/pfaf-data).
- **Acquisition Strategy:**
  - Cloned the SQLite production database archive.
  - Developed an extraction script (`src/pfaf_extractor.py`) to pull rich textual context (cultivation, edibility, medicinal notes) and structured care requirements (hardiness, moisture).
  - **Artifact:** `pfaf_data.jsonl`.
- **License:** CC-BY 4.0.

## 3. Merging & Normalization Logic
- **Tool:** `src/merge_plants.py`.
- **Matching Pipeline:**
  1. **Exact Match:** Author-stripped scientific names are compared across datasets.
  2. **Hierarchical Match:** USDA varieties (e.g., `var. phanerolepis`) that lack specific traits "inherit" data from the parent species entry in PFAF.
  3. **Fuzzy Match:** Leverages the `thefuzz` library ([Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance)) with a high confidence threshold (95%) and a **Token-Length Guard**. The guard ensures that short species names (e.g., *rigida* vs *frigida*) are not incorrectly matched, while valid spelling variations (e.g., *Buddleja* vs *Buddleia*) are caught.
- **Provenance:** Every record in the final output contains an `attributions` array documenting the source database, the original scientific name provided by that source, and the respective license to ensure copyright compliance.
- **Output:** `merged_plants.jsonl` (RAG-optimized JSON structure).

## 4. Dependencies
- **Python Environment:** Managed via `uv`.
- **Key Libraries:** `thefuzz`, `python-Levenshtein`.
