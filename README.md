# itsm-kpi-sla-analytics
## Overview 

Analysis of anonymized, non-synthetic Rabobank IT service desk data from the **2014 BPI Challenge** to practice building real-world SLA-like metrics, KPI reporting, and an ITSM visualization layer that is presented with Excel and Power BI.

**Consists Of:**
- A Python and pandas script that ingests and standardizes large, semicolon-delimited CSV service desk records.
- Relational modeling in SQLite and SQL that suit KPI metric queries and views (e.g., volume, cycle time).
- A quick-reference Excel report of tables constructed from KPI measurements.
- A Power BI dashboard that is constructed from tables that undergo an additional layer of null checks and invalid entries.

## Data Source

Pure CSV data extracted from the **2014 Rabobank BPI Challenge** dataset, which is hosted by **4TU.ResearchData**

**Also: The pure CSV files are not committed to this repository; they are kept locally and entered into `.gitignore` to prevent alteration and distribution.**

### DOIs

Collection DOI (entire dataset):
- **BPI Challenge 2014 (collection):** `https://doi.org/10.4121/uuid:c3e5d162-0cfd-4bb0-bd82-af5268819c35`

Per-file DOIs (as listed by the challenge site):
- **Change records:** `https://doi.org/10.4121/uuid:d5ccb355-ca67-480f-8739-289b9b593aaf` 
- **Incident records:** `https://doi.org/10.4121/uuid:3cfa2260-f5c5-44be-afe1-b70d35288d6d`
- **Interaction records:** `https://doi.org/10.4121/uuid:3d5ae0ce-198c-4b5c-b0f9-60d3035d07bf` 
- **Incident activity records:** `https://doi.org/10.4121/uuid:86977bac-f874-49cf-8337-80f26bf5d2ef`









