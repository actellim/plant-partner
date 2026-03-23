# Data Acquisition & Extraction Process

This document outlines the engineering steps taken to acquire, normalize, and merge the plant characteristic datasets for the Plant Partner project.

## 1. USDA PLANTS Database (Native/North American)
- **Source:** [USDA PLANTS Database Characteristic API](https://plants.sc.egov.usda.gov/home/charSearch).
- **Acquisition Strategy:** 
  - A master symbol list (`plantlst.txt`) was used to iterate through the undocumented internal USDA JSON API.
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
- **Two-Pass Guarded Fuzzy Match:**
  1. **Exact Match:** Author-stripped scientific names are compared across datasets.
  2. **Hierarchical Match:** USDA varieties (e.g., `var. phanerolepis`) that lack specific traits "inherit" data from the parent species entry in PFAF.
  3. **Pass A (Genus):** Identify candidates by performing a fuzzy match on the **Genus string only** with a strict threshold (**90+**). This prevents cross-genus false positives (e.g., *Arabis* vs *Abies*).
  4. **Pass B (Species):** For valid genera, perform a fuzzy match on the **Full Name** (90+ threshold) with an additional **Prefix Guard**.
     - **Prefix Guard:** The first 3 characters of the species epithet must match exactly (e.g., `aug` for `augustum`). This correctly filters out similar but distinct same-genus species (e.g., *Artemisia cana* vs *cina*).
- **Provenance:** Every record in the final output contains an `attributions` array documenting the source database, the original scientific name provided by that source, and the respective license to ensure copyright compliance.
- **Base Artifact:** `merged_plants.jsonl` (Full consolidated dataset of 53,013 records).

## 4. Database Optimization
- **Tool:** `src/filter_plants.py`.
- **Optimization Strategy:** To ensure high-quality RAG results and faster search performance, a high-density subset of the data was created.
  - **Criteria (Strict AND):** A record is only retained if it contains data for **ALL THREE** of the following characteristics (from either source):
    1. **Moisture:** (e.g., `moistureUse`, `precipitationMin`, or `moisture`)
    2. **Temperature:** (e.g., `minTempF` or `hardiness_zone`)
    3. **Light:** (e.g., `shadeTolerance` or `shade`)
  - **Optimized Artifact:** `merged_plants_optimized.jsonl` (11,383 records).

## 5. Dependencies
- **Python Environment:** Managed via `uv`.
- **Key Libraries:** `thefuzz`, `python-Levenshtein`.
