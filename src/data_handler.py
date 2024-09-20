import json
import streamlit as st

def load_data(json_path):
    """Load data from a JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        st.error(f"File not found: {json_path}")
        return []
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON file: {json_path}")
        return []

def extract_unique_names(data):
    """Extract unique names from the loaded data."""
    return [item['uniqueName'] for item in data]