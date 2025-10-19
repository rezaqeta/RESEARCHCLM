import pandas as pd
import os

# Read both Excel files
print("Reading Climate_Behavioral_Change_Papers.xlsx...")
df1 = pd.read_excel('Climate_Behavioral_Change_Papers.xlsx')
print(f"Rows: {len(df1)}")
print(f"Columns: {list(df1.columns)}")
print("\nFirst few rows:")
print(df1.head())
print("\n" + "="*80 + "\n")

print("Reading source_main_cb.xlsx...")
df2 = pd.read_excel('source_main_cb.xlsx')
print(f"Rows: {len(df2)}")
print(f"Columns: {list(df2.columns)}")
print("\nFirst few rows:")
print(df2.head())
print("\n" + "="*80 + "\n")

# Check for PDF-related columns and rows without PDFs
print("Analyzing missing PDFs in Climate_Behavioral_Change_Papers.xlsx:")
pdf_columns = [col for col in df1.columns if 'pdf' in col.lower() or 'file' in col.lower() or 'download' in col.lower()]
print(f"PDF-related columns: {pdf_columns}")
if pdf_columns:
    for col in pdf_columns:
        print(f"\nColumn '{col}' - unique values sample:")
        print(df1[col].value_counts().head(10))

print("\n" + "="*80 + "\n")

print("Analyzing missing PDFs in source_main_cb.xlsx:")
pdf_columns2 = [col for col in df2.columns if 'pdf' in col.lower() or 'file' in col.lower() or 'download' in col.lower()]
print(f"PDF-related columns: {pdf_columns2}")
if pdf_columns2:
    for col in pdf_columns2:
        print(f"\nColumn '{col}' - unique values sample:")
        print(df2[col].value_counts().head(10))



