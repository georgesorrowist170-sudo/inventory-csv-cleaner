from pathlib import Path
import pandas as pd


def create_sample_csv(filepath: str) -> None:
    """Creates the messy initial inventory CSV file inside sample_data."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)  # Creates the directory if missing

    csv_data = """ItemName,Category,Quantity
 milk ,Dairy,20
Bread,Bakery,
Sugar,Grocery,40
 milk ,Dairy,20
Rice,,25
Eggs, Poultry ,60"""

    with open(filepath, "w") as file:
        file.write(csv_data)


def load_inventory(filepath: str) -> pd.DataFrame:
    """Loads the inventory CSV dataset into a Pandas DataFrame."""
    return pd.read_csv(filepath)


def clean_inventory(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the inventory DataFrame by renaming columns, filling missing
    values, stripping extra whitespace, converting data types, and removing duplicates.
    """
    cleaned_df = df.copy()

    # Rename column
    cleaned_df = cleaned_df.rename(columns={"ItemName": "Product"})

    # Fill missing values first so .str.strip() doesn't encounter NaN
    cleaned_df["Category"] = cleaned_df["Category"].fillna("Unknown")
    cleaned_df["Quantity"] = cleaned_df["Quantity"].fillna(0)

    # Strip leading and trailing whitespace
    cleaned_df["Product"] = cleaned_df["Product"].str.strip()
    cleaned_df["Category"] = cleaned_df["Category"].str.strip()

    # Convert Quantity to numeric
    cleaned_df["Quantity"] = pd.to_numeric(cleaned_df["Quantity"])

    # Remove duplicates
    cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)

    return cleaned_df


def print_statistics(df: pd.DataFrame) -> None:
    """Calculates and displays statistics for the cleaned dataset."""
    total_rows = len(df)
    columns = list(df.columns)
    shape = df.shape
    max_qty = df["Quantity"].max()
    avg_qty = df["Quantity"].mean()

    print("\n--- DATASET STATISTICS ---")
    print(f"Total Rows:       {total_rows}")
    print(f"Column Names:     {columns}")
    print(f"Dataset Shape:    {shape}")
    print(f"Highest Quantity: {max_qty}")
    print(f"Average Quantity: {avg_qty:.2f}")


def save_cleaned_inventory(df: pd.DataFrame, output_filepath: str) -> None:
    """Saves the cleaned DataFrame to a CSV file inside the output directory."""
    path = Path(output_filepath)
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensures output dir exists
    df.to_csv(output_filepath, index=False)


def main() -> None:
    input_file = "sample_data/inventory.csv"
    output_file = "output/clean_inventory.csv"

    # Step 1: Create the raw dataset
    create_sample_csv(input_file)

    # Step 2: Load the raw dataset
    original_df = load_inventory(input_file)

    # Step 3: Clean the dataset
    cleaned_df = clean_inventory(original_df)

    # Step 4: Display DataFrames
    print("--- ORIGINAL DATAFRAME ---")
    print(original_df)

    print("\n--- CLEANED DATAFRAME ---")
    print(cleaned_df)

    # Step 5: Display key statistics
    print_statistics(cleaned_df)

    # Step 6: Save the output
    save_cleaned_inventory(cleaned_df, output_file)
    print(f"\nSuccessfully saved cleaned data to '{output_file}'.")


if __name__ == "__main__":
    main()