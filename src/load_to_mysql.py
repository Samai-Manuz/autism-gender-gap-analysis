"""
ETL step: load dimension table into MySQL

This script performs the following steps:
- load processed ASD prevalence dataset from project directory
- validate dataset structure and key fields
- extract unique country values
- insert countries into dim_country table
- retrieve country_id mapping from dim_country table
- map country names to country_id in dataframe
- validate mapping completeness
- insert fact records into fact_asd_prevalence table

Notes:
- region is temporarily set to 'Unknown'
- dim_country uses INSERT IGNORE to avoid duplicate entries
- fact_asd_prevalence uses INSERT IGNORE with a UNIQUE constraint to prevent duplicates
- pipeline is idempotent and can be safely re-executed
"""

# Import core libraries and project paths for data access and processing

import pandas as pd
import mysql.connector

from paths import PROCESSED_DIR


# Establish connection to MySQL database

def get_connection():
    # create database connection using configured credentials
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="asd_analysis"
    )


# Load processed dataset from project directory

def load_data():
    # read processed csv file into dataframe
    file_path = PROCESSED_DIR / "gbd_asd_prevalence_oecd_processed.csv"
    df = pd.read_csv(file_path)
    return df


# Validate data structure before database load

def validate_dataframe(df):
    # check dataframe shape and columns
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    # check for null values in key columns
    print("Nulls per column:")
    print(df.isnull().sum())

    # check unique countries count
    print("Unique countries:", df["country"].nunique())


# Insert unique countries into dim_country table

def load_dim_country(df):
    # establish connection
    conn = get_connection()
    cursor = conn.cursor()

    # extract unique country values
    countries = df["country"].drop_duplicates().tolist()

    # insert countries into dimension table
    for country in countries:
        cursor.execute(
            """
            INSERT IGNORE INTO dim_country (country, region)
            VALUES (%s, %s)
            """,
            (country, "Unknown")
        )

    # commit transaction
    conn.commit()

    # close resources
    cursor.close()
    conn.close()


# Load country_id mapping from dim_country table

def get_country_mapping():
    # establish connection
    conn = get_connection()
    cursor = conn.cursor()

    # fetch country_id and country from dimension table
    cursor.execute("SELECT country_id, country FROM dim_country")
    results = cursor.fetchall()

    # build dictionary mapping country to country_id
    mapping = {country: country_id for country_id, country in results}

    # close resources
    cursor.close()
    conn.close()

    return mapping

# Map country names to country_id in dataframe

def apply_country_mapping(df, mapping):
    # create new column with mapped ids
    df["country_id"] = df["country"].map(mapping)
    return df

# Validate mapping results

def validate_mapping(df):
    # check for unmapped country_id values
    null_ids = df["country_id"].isnull().sum()
    print("Unmapped country_id:", null_ids)


# Insert fact data into fact_asd_prevalence table

def load_fact_table(df):
    # establish connection
    conn = get_connection()
    cursor = conn.cursor()

    # prepare insert query
    query = """
        INSERT IGNORE INTO fact_asd_prevalence
        (year, gender, age_range, prevalence, lower_ui, upper_ui, country_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # convert dataframe rows to tuples
    data = df[
        ["year", "gender", "age_range", "prevalence", "lower_ui", "upper_ui", "country_id"]
    ].values.tolist()

    # execute batch insert
    cursor.executemany(query, data)

    # commit transaction
    conn.commit()

    # close resources
    cursor.close()
    conn.close()


# Main execution flow for ETL step: load dimension and fact tables

if __name__ == "__main__":
    # load dataset
    df = load_data()

    # validate dataset
    validate_dataframe(df)

    # load dimension
    load_dim_country(df)

    # retrieve mapping
    mapping = get_country_mapping()

    # apply mapping
    df = apply_country_mapping(df, mapping)

    # validate mapping
    validate_mapping(df)

    # load fact table
    load_fact_table(df)