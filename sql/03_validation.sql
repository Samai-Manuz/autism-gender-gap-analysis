-- =============================================================================
-- DATA VALIDATION QUERIES
--
-- Purpose:
-- Verify correctness and integrity of loaded data.
--
-- These checks ensure:
-- - expected number of records
-- - absence of duplicates
-- - correct structure of fact table
--
-- Useful for:
-- - debugging ETL processes
-- - validating data before analysis
-- - ensuring reproducibility
-- =============================================================================


-- Validate number of records in dimension table

SELECT COUNT(*) FROM dim_country;


-- Validate number of records in fact table

SELECT COUNT(*) FROM fact_asd_prevalence;


-- Validate absence of duplicate records
-- GROUP BY groups identical records
-- HAVING filters groups with more than 1 occurrence

SELECT 
    year, 
    gender, 
    age_range, 
    country_id, 
    COUNT(*) as cnt
FROM fact_asd_prevalence
GROUP BY 
    year, 
    gender, 
    age_range, 
    country_id
HAVING cnt > 1;


-- Inspect sample of fact data

SELECT * 
FROM fact_asd_prevalence
LIMIT 100;