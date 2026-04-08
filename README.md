## 🔄 Data Pipeline (END-TO-END)

### 1. Data Extraction
- Manual download from GBD (OECD filter)

---

### 2. ETL (Python)
- Cleaning and normalization  
- Country standardization  
- Age bin normalization  

**Metric renaming:**
- val → prevalence
- upper → upper_ui
- lower → lower_ui

---

### 3. Load to MySQL 

Implemented via:

src/load_to_mysql.py

#### ✔ Key characteristics
- ✔ Idempotent pipeline  
- ✔ Uses: INSERT IGNORE  
- ✔ Based on UNIQUE KEY constraint  
- ✔ Safe re-execution (no duplicates)  

---

### 4. Data Warehouse (MySQL)

Database:
asd_analysis

Validated:
- ✔ 38 countries  
- ✔ 38,760 rows in fact table  
- ✔ No duplicates  
- ✔ Full consistency between fact and dimension tables  

---

### 5. Validation Layer (SQL)

Scripts:
- 01_schema.sql → table creation  
- 02_constraints.sql → PK, FK, UNIQUE  
- 03_validation.sql → integrity checks (duplicates, completeness, referential consistency)  

---

### 6. BI Layer — Power BI 

- Connection via native MySQL connector  
- Star schema preserved (no transformations in BI)  

Power BI used strictly as:
- visualization layer  
- analytical interface  

---

## 📈 Analytical Metrics

Computed in pipeline:
- difference → Male − Female  
- ratio → Female / Male  

---

## 📊 Key Findings

- Male prevalence > Female across all dimensions  

Time:
- Absolute gap ↑  
- Relative ratio ↓  

Age:
- Prevalence decreases  
- Gap narrows  

---

## 🔍 Core Insight

A single metric is insufficient to explain the gender gap.

- Absolute and relative metrics must be combined  

---

## ⚠️ Limitations

- Modeled prevalence (not diagnosis timing)  
- Binary sex only  
- No ethnicity segmentation  
- OECD-only scope  

---

## 🚀 Next Steps

- Build Power BI dashboards:
  - Time trends  
  - Age distributions (including life stage aggregation)  
  - Country comparisons  

- Export dashboards for portfolio:
  - .pbix  
  - PDF / PNG  

---

## 📦 Output

reports/figures/

---

## ✔ Project Value

- End-to-end pipeline (ETL → DWH → BI)  
- Real-world data modeling (star schema)  
- Idempotent data engineering practices  
- Clean analytical design  
- Portfolio-ready structure    


