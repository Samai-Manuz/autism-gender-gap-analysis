-- =============================================================================
-- SCHEMA DEFINITION: ASD ANALYSIS DATABASE
--
-- Purpose:
-- Define the relational structure for storing ASD prevalence data
-- following a star schema design (analytical model).
--
-- Design rationale:
-- - dim_country: stores descriptive attributes (dimension table)
-- - dim_age: groups age ranges into life stages (derived dimension)
-- - fact_asd_prevalence: stores measurable events (fact table)
--
-- Benefits:
-- - enables efficient analytical queries
-- - separates descriptive vs measurable data
-- - scalable for BI tools (e.g., Power BI)
-- =============================================================================


-- Create database

CREATE DATABASE IF NOT EXISTS asd_analysis;
USE asd_analysis;


-- Create dimension table for countries
-- Stores unique list of countries and their region

CREATE TABLE IF NOT EXISTS dim_country (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    UNIQUE KEY country_UNIQUE (country)
);


-- Create dimension table for age
-- Groups age ranges into broader life stages for analysis

CREATE TABLE IF NOT EXISTS dim_age (
    age_range VARCHAR(10) PRIMARY KEY,
    life_stage VARCHAR(20) NOT NULL
);


-- Create fact table for ASD prevalence
-- Stores measurements linked to country and time dimensions

CREATE TABLE IF NOT EXISTS fact_asd_prevalence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age_range VARCHAR(10) NOT NULL,
    prevalence DECIMAL(10,2),
    lower_ui DECIMAL(10,2),
    upper_ui DECIMAL(10,2),
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id)
);