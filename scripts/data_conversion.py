import pandas as pd
import json
from collections import defaultdict

def convert_csv_to_json(file_path, output_path):
    """
    Converts a CSV file into a JSON file with a specific format.
    Args:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to save the output JSON file.
    """
    df = pd.read_csv(file_path, dtype=str, low_memory=False)
    
    # Display column names to help users identify any changes
    print("Column names detected in the CSV file:")
    print(df.columns.tolist())
    
    # Clean column names: remove spaces, newlines, and unexpected commas
    df.columns = df.columns.str.strip().str.replace(r'[\r\n]', '', regex=True).str.replace(',', '')
    
    # Drop 'Unnamed' columns
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]
    
    required_columns = ['UniqueName', 'TextDefinition', 'ISO15926-2Entity', 'SuperClass1', 'Classification1']
    
    # Check if required columns are present
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Warning: The following required columns are missing from the CSV: {missing_columns}")
        print("Please update the script to reflect any changes in the CSV file structure.")
        return
    
    data = {}
    
    for _, row in df.iterrows():
        unique_name = row['UniqueName']
        description = row['TextDefinition'] if pd.notna(row['TextDefinition']) else ""
        superclasses = [row[f'SuperClass{i}'] for i in range(1, 6) if f'SuperClass{i}' in df.columns and pd.notna(row[f'SuperClass{i}'])]
        types = [row['ISO15926-2Entity']] + [row[f'Classification{i}'] for i in range(1, 5) if f'Classification{i}' in df.columns and pd.notna(row[f'Classification{i}'])]

        data[unique_name] = {
            "uniqueName": unique_name,
            "description": description,
            "types": ', '.join(filter(None, types)),
            "superclasses": ', '.join(superclasses),
            "subclasses": ""
        }
    
    # Assign subclasses to their respective superclasses
    superclass_dict = defaultdict(list)
    for name, entry in data.items():
        for superclass in entry["superclasses"].split(', '):
            if superclass:
                superclass_dict[superclass].append(name)
    
    # Update subclass field
    for superclass, subclasses in superclass_dict.items():
        if superclass in data:
            data[superclass]["subclasses"] = ', '.join(subclasses)
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(list(data.values()), f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    input_csv = "data/input.csv"  # <-- Change this line if your input file changes
    output_json = "data/final_output.json"  # <-- Change this line if your output file changes
    print("Starting CSV to JSON conversion...")
    convert_csv_to_json(input_csv, output_json)
    print(f"Conversion complete! JSON saved to {output_json}")