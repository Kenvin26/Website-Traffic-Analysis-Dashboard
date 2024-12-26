import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def verify_file_path(file_path):
    """
    Verify if file exists and print helpful messages
    """
    try:
        if os.path.exists(file_path):
            print(f"✓ File found at: {file_path}")
            return True
        else:
            print(f"✕ File not found at: {file_path}")
            print("\nPlease check if:")
            print("1. The path is correct")
            print("2. The file exists in the specified location")
            print("3. The file extension is .csv")
            return False
    except Exception as e:
        print(f"Error checking file path: {str(e)}")
        return False

def load_and_preprocess_data(file_path):
    """
    Load and preprocess website analytics data
    """
    if not verify_file_path(file_path):
        return None
        
    try:
        # Read the CSV file
        print("\nLoading data...")
        df = pd.read_csv(file_path)
        
        # Display initial data info
        print("\nInitial data overview:")
        print(f"Number of rows: {len(df)}")
        print(f"Columns found: {', '.join(df.columns)}")
        
        # Convert date column
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        # Handle numeric columns
        numeric_columns = df.select_dtypes(include=['object']).columns
        for col in numeric_columns:
            try:
                # Remove any '%' signs and convert to float
                if '%' in str(df[col].iloc[0]):
                    df[col] = df[col].str.rstrip('%').astype('float')
                # Remove any time formatting if present
                elif ':' in str(df[col].iloc[0]):
                    # Convert time format to seconds
                    df[col] = pd.to_timedelta(df[col]).dt.total_seconds()
            except:
                continue
        
        # Sort by date
        if 'Date' in df.columns:
            df = df.sort_values('Date')
        
        print("Data preprocessing completed successfully!")
        return df
        
    except Exception as e:
        print(f"\nError in data loading/preprocessing: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure the file is not open in another program")
        print("2. Check if the file is a valid CSV format")
        print("3. Verify you have read permissions for the file")
        print("4. Try copying the file to a simpler path (e.g., Desktop)")
        return None

def main():
    # File path with raw string to handle Windows path
    file_path = r"C:\Users\HP\Downloads\Website_Analytics_20241226.csv"
    
    # Load and preprocess data
    df = load_and_preprocess_data(file_path)
    
    if df is not None:
        print("\nFirst few rows of processed data:")
        print(df.head())
        print("\nData types of columns:")
        print(df.dtypes)
        
        # Save processed data
        try:
            output_path = "processed_website_analytics.csv"
            df.to_csv(output_path, index=False)
            print(f"\nProcessed data saved to: {output_path}")
        except Exception as e:
            print(f"\nError saving processed data: {str(e)}")
    else:
        print("\nCould not proceed with analysis due to data loading error.")

if __name__ == "__main__":
    main()