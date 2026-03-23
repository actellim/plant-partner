## Issue

The perenual db doesn't give water/temp/moisture requirements on the unpaid api. This leaves two primary candidates: the USDA PLANTS database and the OpenFarm Database Archive.

## Solution

We need to grab the raw data from these databases and do our best to merge it. This may require renaming fields, we need to create an E-R diagram for both.

## Steps

1. Find and download USDA PLANTS database.
  - The data they provide for download is incomplete.
  - May need to scrape data from [their search tool](https://plants.sc.egov.usda.gov/characteristics-search).
2. ~~Find and download OpenFarm Database Archive.~~
  - ~~Their archived [Git Repo](https://github.com/openfarmcc/OpenFarm.git) is probably the place to start chasing down the loose ends to find the database.~~
  - Their repo doesn't contain a complete database; it's necessary to pivot.
3. Plants for a Future is CC-4.0 attribution licensed, and there's a scrape of it on [GitHub](https://github.com/saulshanabrook/pfaf-data?tab=readme-ov-file).
  - Perfect! It's in a different format than USDA, but we can merge.
4. Inspect the files.
  - We need species, moisture, light, and temperature data.
  - USDA provides an incomplete dataset.
    - Should be possible to match USDA Genius with Species from PFAF to get better coverage.
5. Create an E-R diagram using plantUML detailing the expected data structures.
6. Merge data into a single monolithic CC database with proper attribution.
7. Remove entries with incomplete care requirements.
8. Convert the `.jsonl` object into a database object.
