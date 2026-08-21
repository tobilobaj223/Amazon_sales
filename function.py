import pandas as pd
def read_csv_file(file_path):
    return pd.read_csv(file_path)


def show_sample(df, rows=5):
    print(f"\n--- FIRST {rows} ROWS ---")
    print(df.head(rows))


def show_dataset_info(df):
    print("\n--- DATASET SHAPE ---")
    print(df.shape)

    print("\n--- COLUMN NAMES ---")
    print(df.columns.tolist())
    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- DUPLICATE ROWS ---")
    print(df.duplicated().sum())    

def show_column_summary(df):
    print("\n--- COLUMN SUMMARY ---")

    summary = pd.DataFrame({
        'Column Name': df.columns,
        'Data_Type': df.dtypes.astype(str).values,
        'Missing_Values': df.isnull().sum().values, 
        'Unique_Values': df.nunique().values
    })  

    print(summary.to_string(index=False))

def inspect_numeric_columns(df):
    print("\n--- NUMERIC COLUMNS SAMPLES--")

    columns = [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
    ]

    for columns in columns:
        print(f"\n{columns}:")
        print(df[columns].dropna().head(10).to_list())

def find_missing_data(df):
    """
    find rows containing missing values.
    """
    missing_rows = df[df.isnull().any(axis=1)].copy()
    return missing_rows

def save_missing_data(df, Output_path):

    missing_rows = df[df.isnull().any(axis=1)].copy()
    missing_rows["rejected_reason"] = "Missing rating_count"
    missing_rows.to_csv(Output_path, index=False)
    return missing_rows


def find_invalid_data(df):
    """
    validate numeric-looking columns and return invalid rows.
    The raw data is not modified.
    """
    invalid_mask = pd.Series(False, index=df.index)

    rating_raw = df["rating"].astype(str).str.strip()
    rating = pd.to_numeric(rating_raw, errors="coerce")

    invalid_rating_format = (
        df["rating"].notna() &
        rating.isna()
    )

    invalid_rating = (
            rating.notna() &
            ((rating < 0) | (rating > 5))
    )

    # validate discount percentage

    discount_raw = (
        df["discount_percentage"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    discount = pd.to_numeric(discount_raw, errors="coerce")

    invalid_discount_range = (
        discount.notna() &
        ((discount < 0) | (discount > 100))
    )

    #validate dicounted price
    discounted_raw = (
        df["discounted_price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    discounted_price = pd.to_numeric(
        discounted_raw,
        errors="coerce"
    )

    invalid_discounted_format = (
        df["discounted_price"].notna() &
        discounted_price.isna()
    )

    invalid_discounted_range = (
        discounted_price.notna() &
        (discounted_price < 0)
    )

    #validate actual price
    actual_raw = (
        df["actual_price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    actual = pd.to_numeric(
        actual_raw,
        errors="coerce"
    )
    invalid_actual_format = (
        df["actual_price"].notna() &
        actual.isna()
    )

    invalid_actual_range = (
        actual.notna() &
        (actual < 0)
    )

    #validate rating count
    rating_count_raw = (
        df["rating_count"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    rating_count = pd.to_numeric(
        rating_count_raw,
        errors="coerce"
    )
    invalid_rating_count_format = (
        df["rating_count"].notna() &
        rating_count.isna()
    )

    invalid_rating_count_range = (
        rating_count.notna() &
        (rating_count < 0)
    )

    #combine all validation failures
    invalid_mask = (
        invalid_rating_format
        | invalid_rating_count_range 
        | invalid_discounted_format
        | invalid_discounted_range
        | invalid_discounted_format
        | invalid_discounted_range
        | invalid_actual_format
        | invalid_actual_range
        | invalid_rating_count_format
        | invalid_rating_count_range
    )

    invalid_rows = df[invalid_mask].copy()
    return invalid_rows

def add_rejection_reasons(df):
    """
    Identify why each row is rejected.
    The raw data is not changed.
    """

    rejected = df.copy()

    reasons = []

    for _, row in rejected.iterrows():

        row_reasons = []

        # -----------------------------
        # Missing-value checks
        # -----------------------------

        if pd.isna(row["product_id"]) or str(row["product_id"]).strip() == "":
            row_reasons.append("missing_product_id")

        if pd.isna(row["product_name"]) or str(row["product_name"]).strip() == "":
            row_reasons.append("missing_product_name")

        if pd.isna(row["category"]) or str(row["category"]).strip() == "":
            row_reasons.append("missing_category")

        if pd.isna(row["discounted_price"]) or str(row["discounted_price"]).strip() == "":
            row_reasons.append("missing_discounted_price")

        if pd.isna(row["actual_price"]) or str(row["actual_price"]).strip() == "":
            row_reasons.append("missing_actual_price")

        if pd.isna(row["discount_percentage"]) or str(row["discount_percentage"]).strip() == "":
            row_reasons.append("missing_discount_percentage")

        if pd.isna(row["rating"]) or str(row["rating"]).strip() == "":
            row_reasons.append("missing_rating")

        if pd.isna(row["rating_count"]) or str(row["rating_count"]).strip() == "":
            row_reasons.append("missing_rating_count")

        # -----------------------------
        # Invalid rating
        # -----------------------------

        if pd.notna(row["rating"]):

            try:
                rating = float(str(row["rating"]).strip())

                if rating < 0 or rating > 5:
                    row_reasons.append("invalid_rating_range")

            except ValueError:
                row_reasons.append("invalid_rating_format")

        # -----------------------------
        # Invalid discount percentage
        # -----------------------------

        if pd.notna(row["discount_percentage"]):

            value = str(row["discount_percentage"]).strip()

            if not value.endswith("%"):
                row_reasons.append("invalid_discount_format")
            else:
                try:
                    discount = float(value.replace("%", ""))

                    if discount < 0 or discount > 100:
                        row_reasons.append("invalid_discount_range")

                except ValueError:
                    row_reasons.append("invalid_discount_format")

        # -----------------------------
        # Invalid discounted price
        # -----------------------------

        if pd.notna(row["discounted_price"]):

            value = str(row["discounted_price"]).strip()
            value = value.replace("₹", "").replace(",", "").strip()

            try:
                price = float(value)

                if price < 0:
                    row_reasons.append("invalid_discounted_price_range")

            except ValueError:
                row_reasons.append("invalid_discounted_price_format")

        # -----------------------------
        # Invalid actual price
        # -----------------------------

        if pd.notna(row["actual_price"]):

            value = str(row["actual_price"]).strip()
            value = value.replace("₹", "").replace(",", "").strip()

            try:
                price = float(value)

                if price < 0:
                    row_reasons.append("invalid_actual_price_range")

            except ValueError:
                row_reasons.append("invalid_actual_price_format")

        # -----------------------------
        # Invalid rating count
        # -----------------------------

        if pd.notna(row["rating_count"]):

            value = str(row["rating_count"]).strip()
            value = value.replace(",", "")

            try:
                count = float(value)

                if count < 0:
                    row_reasons.append("invalid_rating_count_range")

            except ValueError:
                row_reasons.append("invalid_rating_count_format")

        # -----------------------------
        # Store reasons
        # -----------------------------

        reasons.append(", ".join(row_reasons))


    rejected["rejection_reason"] = reasons

    # Keep only rows that actually have a reason
    rejected = rejected[
        rejected["rejection_reason"] != ""
    ].copy()

    return rejected

