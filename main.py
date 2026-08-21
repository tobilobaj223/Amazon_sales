import os
import logging
import pandas as pd

from function import (
    read_csv_file,
    show_sample,
    show_dataset_info,
    show_column_summary,
    inspect_numeric_columns,
    find_missing_data,
    save_missing_data,
    find_invalid_data,
    add_rejection_reasons
)


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

os.makedirs("Output", exist_ok=True)

logging.basicConfig(
    filename="Output/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("Amazon data pipeline started.")


# ============================================================
# A. LOAD RAW AMAZON DATA
# ============================================================

file_path = "Data/amazon.csv"

df = read_csv_file(file_path)

logger.info(
    f"Raw dataset loaded: {len(df)} rows, {len(df.columns)} columns."
)

print("\n--- RAW AMAZON DATA LOADED ---")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# B. INITIAL DATA INSPECTION
# ============================================================

print("\n========== DATA INSPECTION ==========")

# First 5 rows
print("\n--- FIRST 5 ROWS ---")
show_sample(df)


# Dataset shape, columns, data types,
# missing values and duplicate rows
print("\n--- DATASET INFORMATION ---")
show_dataset_info(df)


# Column-level summary
print("\n--- COLUMN SUMMARY ---")
show_column_summary(df)


# Numeric column inspection
print("\n--- NUMERIC COLUMN INSPECTION ---")
inspect_numeric_columns(df)


# ============================================================
# C. DATA VALIDATION
# ============================================================

print("\n========== DATA VALIDATION ==========")


# ------------------------------------------------------------
# 1. FIND MISSING DATA
# ------------------------------------------------------------

missing_data = find_missing_data(df)

logger.info(
    f"Missing data identified: {len(missing_data)} rows."
)

print("\n--- ROWS WITH MISSING VALUES ---")

if not missing_data.empty:
    print(missing_data)
else:
    print("No missing data found.")


# Save missing data
save_missing_data(
    missing_data,
    "Output/missing_data.csv"
)

logger.info("missing_data.csv generated successfully.")

print("\n--- MISSING DATA FILE GENERATED ---")
print("File: Output/missing_data.csv")
print(f"Rows saved: {len(missing_data)}")


# ------------------------------------------------------------
# 2. FIND INVALID DATA
# ------------------------------------------------------------

invalid_data = find_invalid_data(df)

logger.info(
    f"Invalid data identified: {len(invalid_data)} rows."
)

print("\n--- INVALID DATA ---")
print(f"Invalid rows found: {len(invalid_data)}")

if not invalid_data.empty:
    print(invalid_data)
else:
    print("No invalid data found.")


# Save invalid data
invalid_data.to_csv(
    "Output/invalid_data.csv",
    index=False
)

logger.info("invalid_data.csv generated successfully.")

print("\n--- INVALID DATA FILE GENERATED ---")
print("File: Output/invalid_data.csv")
print(f"Rows saved: {len(invalid_data)}")


# ------------------------------------------------------------
# 3. CREATE REJECTED ROWS WITH REASONS
# ------------------------------------------------------------

rejected_rows = add_rejection_reasons(df)

logger.info(
    f"Total rejected rows identified: {len(rejected_rows)}."
)


rejected_rows.to_csv(
    "Output/rejected_rows.csv",
    index=False
)

logger.info("rejected_rows.csv generated successfully.")

print("\n--- REJECTED DATA FILE GENERATED ---")
print("File: Output/rejected_rows.csv")
print(f"Rows saved: {len(rejected_rows)}")


# Show rejection reasons
print("\n--- REJECTION REASONS ---")

if not rejected_rows.empty:

    print(
        rejected_rows[
            ["product_id", "rejection_reason"]
        ].to_string(index=False)
    )

else:

    print("No rejected rows found.")


# ------------------------------------------------------------
# 4. CREATE CLEAN AMAZON DATA
# ------------------------------------------------------------

clean_amazon = df.drop(
    index=rejected_rows.index
)


clean_amazon.to_csv(
    "Output/clean_amazon.csv",
    index=False
)

logger.info(
    f"Clean Amazon dataset generated: {len(clean_amazon)} rows."
)

logger.info("clean_amazon.csv generated successfully.")

print("\n--- CLEAN AMAZON DATA FILE GENERATED ---")
print("File: Output/clean_amazon.csv")
print(f"Rows saved: {len(clean_amazon)}")


# ============================================================
# D. DATA QUALITY REPORT
# ============================================================

duplicate_rows = df.duplicated().sum()

data_quality_report = pd.DataFrame({
    "check": [
        "raw_rows",
        "raw_columns",
        "duplicate_rows",
        "missing_data_rows",
        "invalid_data_rows",
        "rejected_rows",
        "clean_rows"
    ],
    "result": [
        len(df),
        len(df.columns),
        duplicate_rows,
        len(missing_data),
        len(invalid_data),
        len(rejected_rows),
        len(clean_amazon)
    ]
})


report_file = "Output/data_quality_report.csv"

data_quality_report.to_csv(
    report_file,
    index=False
)

logger.info(
    "data_quality_report.csv generated successfully."
)

print("\n--- DATA QUALITY REPORT GENERATED ---")
print(f"File: {report_file}")

print("\n--- DATA QUALITY REPORT ---")
print(
    data_quality_report.to_string(index=False)
)


# ============================================================
# E. FINAL PIPELINE SUMMARY
# ============================================================

print("\n========== FINAL PIPELINE SUMMARY ==========")

print(f"Raw rows:                 {len(df)}")
print(f"Raw columns:              {len(df.columns)}")
print(f"Duplicate rows:           {duplicate_rows}")
print(f"Missing-data rows:        {len(missing_data)}")
print(f"Invalid-data rows:        {len(invalid_data)}")
print(f"Rejected rows:            {len(rejected_rows)}")
print(f"Clean Amazon rows:        {len(clean_amazon)}")


print("\n--- OUTPUT FILES ---")

print("Output/missing_data.csv")
print("Output/invalid_data.csv")
print("Output/rejected_rows.csv")
print("Output/clean_amazon.csv")
print("Output/data_quality_report.csv")
print("Output/pipeline.log")


logger.info("Amazon data pipeline completed successfully.")


print("\nData validation and separation completed.")
print("The original Data/amazon.csv was not modified.")