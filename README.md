# itsm-kpi-sla-analytics
## Overview 

Analysis of anonymized, non-synthetic Rabobank IT service desk data from the **2014 BPI Challenge** to practice building real-world SLA-like metrics, KPI reporting, and an ITSM visualization layer that is made appropriate for Excel and Power BI.

**Consists Of:**
- A Python and pandas script that ingests and standardizes large, semicolon-delimited CSV service desk records.
- Relational modeling in SQLite and SQL that suit KPI metric queries and views (e.g., volume, cycle time).
- A quick-reference Excel report of tables constructed from KPI measurements.
- A Power BI dashboard that is constructed from tables that undergo an additional layer of null checks and invalid entries.

## Data Source

Pure CSV data extracted from the **2014 Rabobank BPI Challenge** dataset, which is hosted **4TU.ResearchData**

**Also: The pure CSV files are not committed to this repository; they are kept locally and entered into '.gitignore" to prevent alteration and distribution.











