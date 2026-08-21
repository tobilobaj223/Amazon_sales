# Amazon_sales
This project was developed as a small data quality and validation pipeline.
The workflow starts with raw Amazon dataset and processes the data through several validation and quality_control stages.

### 1. Data Ingestion

The pipeline begins by loading the raw Amazon CSV file from the 'Data/'directory.

    '''python
    file_path = "Data/amazon.csv"
    df = read_csv_file(file_path)


The raw dataset is loaded into a pandas DataFrame for inspection and validation.
The original amazon.csv file is never modified.

### 2. Data Inspection

After ingestion, the dataset is profiled before validation.

The pipeline checks:

                • Number of rows
                • Number of columns
                • Column names
                • Data types
                • Missing values
                • Duplicate rows
                • Unique values

The first records are also displayed to understand the structure of the dataset.

### 3. Numeruc column Inspection
The numeric fields are inspected separately because some valuesbare stored as strings in the raw Amazon dataset.

The following fields are examined:

                                • discounted_price
                                • actual_price
                                 discount_percentage
                                • rating
                                • rating_count
    This helps identify values that may have formatting or validation problems before they clasasies as invalid.

### 4. Missing Data Detection

The pipeline identifies records containing missing values

for example, the raw dataset contains missing values in the rating_count column.

Missing records are separated from the raw dataset and written to:

       Output/missing_data.csv

The missing values are not filled or changed because the objectives of this project is to identify and separate problematic records rather than modify the original data

### 5. Rejection Reason Tracking
A rejected record should not only be identified; the reason for rejection should also nbe understandable.

The pipeline therefore assigns rejection reasons to problematic records.

    examples:
            missing_rating_count
            invalid_rating
            ivalid_rating_count_format
            iv=nvalid_rating_count_range
            invalid_discounted_format
            invalid_discounted_range
            invalid_actual_format
            invalid_actual_range
Theese reasoms are stored with the rejected records in:

     Output/rejected_rows.csv

### 6. REJECTED DATA SEPARATION

Missing ad invalid records are combined into a rejected dataset

The rejected records are separated from the valid records without changing the original dataset

### 7

After indentifying the rejected records, the pipeline creates a clean dataset containing records that passed the validation process.

The resulting file is:
The clean dataset is geerated separately from the raw source file,.

### 8 CLEAN DATA GENERATION
After identifying the rejected records, the pipeline creates a clean dataet containing records that passed the validation process.

The resulting file is:
    
    Output/clean_amazon.csv


The clean dataset is generated separately from the raw source file.

### 9 DATA QUALITY REPORTING
The pipeline generates a data quality report to provide a summary of the validation process.

The report includes information such as:

• Total raw rows
• Total columns
• Duplicate rows
• Missing-data rows
• invalid-data rows
• Rejected rows
• Clean rows

The report is stored in:

    Output/data_quality_report.csv

A Summary file is also generated:

    Output/data_quality_summary.csv

### 10 Logging
Logging was added to make the pipeline easier to monitor and troubleshoot.
The pipeline records events such as:
• pipeline starts
• Dataset loading
• Number of records loaded
• Missing reords identified
• Invalid records identified
• Output files generated

The log file is stored at:
                 
     Output/pipeline.log

### 11 MODULAR PYTHON FUNTIONS
The pipeline was designed using reusable python functions instead of putting all processing logic inside one large script.
The main reusable functions include:

    read_cv_file()
    show_sample()
    show_datatset_info()
    show_column_summary()
    inspect_numeric_columns()
    find_missing_data()
    save_missing_data()
    find_invalid_data()
    add_rejection_reasons()
The main.pyfile coordinates the pipeline, whike the reusable processing logic is maintained in function.py.
This makes the project easier to read, test, maintain, and extend.

### 12 TESTING
Basic test are used to verify important validation function
The purpose of the tests is to confirm that:

• Missing records are detected correctly
• Invalid records are detected correctly
• Rejection logic works as expected
• Valid Records are separated from rejected records
• Changes tot the pipeline do not unintentionally break existing logic.

### 13 RAW DATA PRESERVATION
An important desihn decision in this project is that the raw source data is never overwritten
The pipeline follows this patterns 

    Raw Data
       |
       v
    Inspection
       |
       v
    Validation
       |
     +------------------+
        |                  |
       v                  v
    Missing Data      Invalid Data
       |                  |
       +--------+---------+
                |
                v
          Rejected Rows
                |
                v
          Clean Dataset
                |
                v
       Data Quality Report

This allows rejected reocrds to be investigated while keeping the original source data avilable for traceability.
