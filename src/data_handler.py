import json
import os

def load_data():
    """Load the dataset from JSON file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'data', 'final_output.json')

    with open(json_path) as json_file:
        data = json.load(json_file)

    return data