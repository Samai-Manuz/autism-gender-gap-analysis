"""
ETL step: load dimension tables and fact table into MySQL

This script performs the following steps:
- load processed ASD prevalence dataset from project directory
- validate dataset structure and key fields
- extract unique country values
- insert countries into dim_country table
- insert age ranges into dim_age table with life stage classification
- retrieve country_id mapping from dim_country table
- map country names to country_id in dataframe
- validate mapping completeness
- validate that all age_range values exist in dim_age
- insert fact records into fact_asd_prevalence table

Notes:
- region is temporarily set to 'Unknown'
- dim_country uses INSERT IGNORE to avoid duplicate entries
- dim_age uses INSERT IGNORE to ensure idempotent loading
- fact_asd_prevalence uses INSERT IGNORE with a UNIQUE constraint to prevent duplicates
- pipeline is idempotent and can be safely re-executed
"""

import pandas as pd
import mysql.connector

from paths import PROCESSED_DIR


# Establish connection to MySQL database

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="asd_analysis"
    )


# Load processed dataset from project directory

def load_data():
    file_path = PROCESSED_DIR / "gbd_asd_prevalence_oecd_processed.csv"
    df = pd.read_csv(file_path)
    return df


# Validate data structure before database load

def validate_dataframe(df):
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    print("Nulls per column:")
    print(df.isnull().sum())

    print("Unique countries:", df["country"].nunique())


# Insert unique countries into dim_country table

def load_dim_country(df):
    conn = get_connection()
    cursor = conn.cursor()

    countries = df["country"].drop_duplicates().tolist()

    for country in countries:
        cursor.execute(
            """
            INSERT IGNORE INTO dim_country (country, region)
            VALUES (%s, %s)
            """,
            (country, "Unknown")
        )

    conn.commit()
    cursor.close()
    conn.close()


# Insert age ranges into dim_age table with life stage classification

def load_dim_age():
    conn = get_connection()
    cursor = conn.cursor()

    dim_age_data = [
        ("<5", "Childhood"),
        ("5-9", "Childhood"),
        ("10-14", "Adolescence"),
        ("15-19", "Adolescence"),
        ("20-24", "Youth"),
        ("25-29", "Youth"),
        ("30-34", "Adulthood"),
        ("35-39", "Adulthood"),
        ("40-44", "Adulthood"),
        ("45-49", "Adulthood"),
        ("50-54", "Adulthood"),
        ("55-59", "Adulthood"),
        ("60-64", "Senior"),
        ("65-69", "Senior"),
        ("70+", "Senior")
    ]

    cursor.executemany(
        """
        INSERT IGNORE INTO dim_age (age_range, life_stage)
        VALUES (%s, %s)
        """,
        dim_age_data
    )

    conn.commit()
    cursor.close()
    conn.close()


# Load country_id mapping from dim_country table

def get_country_mapping():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT country_id, country FROM dim_country")
    results = cursor.fetchall()

    mapping = {country: country_id for country_id, country in results}

    cursor.close()
    conn.close()

    return mapping


# Map country names to country_id in dataframe

def apply_country_mapping(df, mapping):
    df["country_id"] = df["country"].map(mapping)
    return df


# Validate country mapping results

def validate_mapping(df):
    null_ids = df["country_id"].isnull().sum()
    print("Unmapped country_id:", null_ids)


# Validate that all age_range values exist in dim_age

def validate_age_dimension(df):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT age_range FROM dim_age")
    dim_ages = {row[0] for row in cursor.fetchall()}

    df_ages = set(df["age_range"].unique())

    missing = df_ages - dim_ages

    print("Missing age_range in dim_age:", missing)

    cursor.close()
    conn.close()


# Insert fact data into fact_asd_prevalence table

def load_fact_table(df):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT IGNORE INTO fact_asd_prevalence
        (year, gender, age_range, prevalence, lower_ui, upper_ui, country_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    data = df[
        ["year", "gender", "age_range", "prevalence", "lower_ui", "upper_ui", "country_id"]
    ].values.tolist()

    cursor.executemany(query, data)

    conn.commit()
    cursor.close()
    conn.close()


# Main execution flow for ETL step: load dimension and fact tables

if __name__ == "__main__":
    df = load_data()

    validate_dataframe(df)

    load_dim_country(df)
    load_dim_age()

    mapping = get_country_mapping()

    df = apply_country_mapping(df, mapping)

    validate_mapping(df)
    validate_age_dimension(df)

    load_fact_table(df)