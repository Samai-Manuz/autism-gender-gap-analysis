# Autism Gender Gap Analysis (OECD · GBD/IHME)

**End-to-end analysis of ASD prevalence by gender, age, and geography**, evolving from exploratory analysis to a structured **data warehouse (star schema) + BI layer**.

---

## 🎯 Objective

To analyze gender differences in ASD prevalence and evaluate how they vary:

* across **age groups**
* over **time**
* across **countries** and **regions**

With a focus on:

> Identifying patterns consistent with **potential late diagnosis in women** using robust, reproducible data pipelines.

---

## 📊 Data Strategy

### ✔ Core dataset — IHME Global Burden of Disease (GBD)

* Global coverage
* Standardized methodology
* Segmentation: country · year · sex · age
* Time series: **1990–2023**

**Limitation:**

* Modeled prevalence (not diagnosis timing)

---

## 🌍 Country Selection

✔ OECD countries selected:

* Comparable healthcare systems
* Similar diagnostic infrastructure
* Better cross-country consistency

---

## 🧱 Data Architecture 

The project evolves from notebook-based analysis to a **star schema in MySQL**:

### 🔹 Dimension table

**dim_country**

* `country_id` (PK)
* `country`
* `region`

---

### 🔹 Fact table

**fact_asd_prevalence**

* `id` (PK)
* `year`
* `gender`
* `age_range`
* `prevalence`
* `lower_ui`
* `upper_ui`
* `country_id` (FK → dim_country)

---

### 🔹 Model characteristics

* ✔ Star schema (dim → fact)
* ✔ 1:N relationship
* ✔ Analytical grain:

```
(year, gender, age_range, country)
```

* ✔ Unique constraint enforced:

```
UNIQUE(year, gender, age_range, country_id)
```

---

## 🧱 Repository Structure 

```text
autism-diagnosis-gender-gap/
│
├── data/
│   ├── 1_raw/
│   ├── 2_interim/
│   └── 3_processed/
│
├── notebooks/
│   ├── 01_gbd_download_oecd.ipynb
│   ├── 02_asd_etl_oecd.ipynb
│   ├── 03_metrics_sex_age.ipynb
│   └── 04_analysis_visuals.ipynb
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_constraints.sql
│   └── 03_validation.sql
│
├── src/
│   ├── paths.py
│   └── load_to_mysql.py
│
├── reports/
│   └── figures/
```

---

## 🔄 Data Pipeline (END-TO-END)

### 1. Data Extraction

* Manual download from GBD (OECD filter)

---

### 2. ETL (Python)

* Cleaning and normalization
* Country standardization
* Age bin normalization
* Metric renaming:

  * `val → prevalence`
  * `upper → upper_ui`
  * `lower → lower_ui`

---

### 3. Load to MySQL 

Implemented via:

```bash
src/load_to_mysql.py
```

#### ✔ Key characteristics

* ✔ Idempotent pipeline
* ✔ Uses:

```sql
INSERT IGNORE
```

* ✔ Based on UNIQUE KEY constraint
* ✔ Safe re-execution (no duplicates)

---

### 4. Data Warehouse (MySQL)

Database:

```
asd_analysis
```

Validated:

* ✔ 38 countries
* ✔ 38,760 rows in fact table
* ✔ No duplicates

---

### 5. Validation Layer (SQL)

Scripts:

* `01_schema.sql` → table creation
* `02_constraints.sql` → PK, FK, UNIQUE
* `03_validation.sql` → integrity checks

---

### 6. BI Layer — Power BI 

* Connection via native MySQL connector
* Star schema preserved (no transformations in BI)
* Power BI used strictly as:

  * visualization layer
  * analytical interface

---

## 📈 Analytical Metrics

Computed in pipeline:

* **difference** → Male − Female
* **ratio** → Female / Male

---

## 📊 Key Findings

* Male prevalence > Female across all dimensions

**Time:**

* Absolute gap ↑
* Relative ratio ↓

**Age:**

* Prevalence decreases
* Gap narrows

---

## 🔍 Core Insight

> A single metric is insufficient to explain the gender gap.

* Absolute and relative metrics must be combined

---

## ⚠️ Limitations

* Modeled prevalence (not diagnosis timing)
* Binary sex only
* No ethnicity segmentation
* OECD-only scope

---

## 🚀 Next Steps

* Build Power BI dashboards:

  * Time trends
  * Age distributions
  * Country comparisons
* Export dashboards for portfolio:

  * `.pbix`
  * PDF / PNG

---

## 📦 Output

```text
reports/figures/
```

---

## ✔ Project Value

* End-to-end pipeline (ETL → DWH → BI)
* Real-world data modeling (star schema)
* Idempotent data engineering practices
* Clean analytical design
* Portfolio-ready structure
