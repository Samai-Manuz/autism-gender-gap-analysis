# Autism Gender Gap Analysis (OECD · GBD/IHME)

**End-to-end analysis of ASD prevalence by gender, age, and geography** using Global Burden of Disease (IHME) data.

This project is designed to demonstrate:
- analytical rigor  
- structured decision-making  
- reproducible and scalable data workflows  

---

## 🎯 Objective

To analyze gender differences in ASD prevalence and evaluate how they vary:

- across **age groups**  
- over **time**  
- across **countries** and **regions**  

With a specific focus on:

> Exploring whether observed gender gaps may be partially explained by **late diagnosis in women**.

---

## 👤 Context

I am **Samai Manuz Rodríguez**, a late-diagnosed autistic woman.

This project is also motivated by a well-documented issue in research:

> Autism in women is often underdiagnosed or diagnosed later in life.

The approach is **analytical (not clinical)**:  
data is used to identify patterns consistent with this hypothesis, not to establish causality.

---

## 📊 Data Strategy

### ✔ Core dataset — IHME Global Burden of Disease (GBD)

Selected because it provides:

- global coverage  
- standardized methodology  
- segmentation by country, year, sex and age  
- long-term time series (1990–2023)  

**Key limitation:**
- uses **modeled prevalence**, not real **diagnosis timing**

👉 Best available backbone for **international comparability**

---

## 🔎 Sources considered (global analysis)

Several institutional sources were evaluated using strict criteria (coverage, segmentation, comparability, methodology):

- **WHO (World Health Organization)** → too aggregated, low granularity  
- **CDC (ADDM, United States)** → high quality but single-country scope  
- **Eurostat** → proxy variables, not direct ASD diagnosis  
- **ECDC** → heterogeneous and not ASD-specific  
- **National datasets (UK, Australia, INE, etc.)** → not comparable across countries  

### 🔴 Key conclusion

> There is currently no global, standardized dataset that provides ASD diagnosis by year + sex + age.

👉 Therefore, a **layered approach** is used:
- GBD → global comparability  
- other sources → contextual support  

---

## 🌍 Country Selection Strategy

Different approaches were evaluated:

- **GBD SDI (Socio-Demographic Index)** → continuous but less interpretable  
- **World Bank (High-income countries)** → categorical and less flexible  
- **OECD countries** → ✔ **selected**

### ✔ Why OECD

- comparable healthcare systems  
- similar diagnostic capacity  
- better structural consistency  

---

### ⚠️ Data extraction constraint

Attempts to use scraping/APIs were blocked by anti-bot policies.

### ✔ Solution

Manual extraction and dataset creation:

data/3_processed/oecd_members.csv

---

## 🌐 Regional Aggregation

Custom dataset grouping OECD countries into regions:

data/3_processed/oecd_regions.csv

---

## 🧱 Repository Structure

autism-gender-gap-analysis/
│
├── data/
│ ├── 1_raw/
│ ├── 2_interim/
│ └── 3_processed/
│
├── notebooks/
│ ├── 01_gbd_download_oecd.ipynb
│ ├── 02_asd_etl_oecd.ipynb
│ ├── 03_metrics_sex_age.ipynb
│ └── 04_analysis_visuals.ipynb
│
├── reports/
│ └── figures/
│
├── src/
│ └── paths.py

> Minimal `src` by design (no over-engineering).

---

## 🔄 Data Pipeline

1. Download (GBD extraction)  
2. ETL (cleaning, normalization, validation)  
3. Metrics:
   - **difference** → absolute gap (Male − Female)  
   - **ratio** → relative relationship (Female / Male)  
   - **pct** → computed but excluded (redundant)  
4. Analysis and visualization  

---

## 📈 Key Findings

- Male prevalence > Female across all dimensions  

**Over time:**
- Difference ↑ (absolute gap widens)  
- Ratio ↓ (female share declines)  

**With age:**
- Prevalence decreases  
- Absolute gap narrows  

---

## 🔍 Core Insight

> The gender gap cannot be described using a single metric.

- Difference and ratio provide **complementary perspectives**  
- Both are required for correct interpretation  

---

## ⚠️ Scope & Limitations

- Uses **modeled prevalence**, not diagnosis timing  
- Gender limited to **biological sex**  
- No segmentation by gender identity  
- No race/ethnicity due to lack of comparable global data  

---

## 🚀 Next Steps

- Power BI / Tableau dashboards (interactive analysis)  

### ✔ Hypothesis to explore

> Higher relative prevalence in adult women → potential signal of late diagnosis  

### ✔ Scalability

- extend beyond OECD  
- integrate clinical/diagnostic datasets (when available)  
  - key challenge: matching global coverage + sex/age/time segmentation  

---

## 📦 Output

All figures are exported to:

reports/figures/

---

## ✔ Project Value

- structured analytical thinking  
- clear decision framework  
- iterative problem-solving  
- reproducible workflow + clean visuals  