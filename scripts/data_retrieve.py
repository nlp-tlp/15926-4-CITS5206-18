import pandas as pd
from SPARQLWrapper import SPARQLWrapper, CSV
import csv
import io
import json
import traceback

# Function to replace HTML entities like &lt; and &gt; with < and >
def replace_html_entities(text):
    return text.replace('&lt;', '<').replace('&gt;', '>')

# Initialize the SPARQL endpoint
sparql = SPARQLWrapper("http://190.92.134.58:8890/sparql")
# Set a timeout to prevent hanging queries (in seconds)
sparql.setTimeout(60)  # Adjust as needed

# Initialize an empty dictionary to hold the data
data = {}

# Define the batch size for pagination
batch_size = 5000  # Adjust based on endpoint limitations
# Initialize the last uniqueName retrieved to an empty string
last_unique_name = ""
# Flag to control the pagination loop
more_data = True

# Loop to paginate through all the data using keyset pagination
while more_data:
    print(f"Processing batch starting after '{last_unique_name}'")
    # Build the FILTER condition for keyset pagination
    if last_unique_name:
        # If last_unique_name is not empty, filter to get records after it
        pagination_filter = f'FILTER (STR(?uniqueName) > "{last_unique_name}")'
    else:
        # If it's the first batch, no filter is needed
        pagination_filter = ''
    
    # Construct the SPARQL query
    query = f"""
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix meta: <http://data.15926.org/meta/>
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?uniqueName ?superClassName ?description ?type ?subClassName
    WHERE {{
      # Retrieve the label (uniqueName) of the class
      ?class rdfs:label ?uniqueName .
      {pagination_filter}  # Apply the pagination filter if needed

      # Optionally retrieve the definition (description) of the class
      OPTIONAL {{
        ?class skos:definition ?description .
      }}

      # Optionally retrieve the superclass name
      OPTIONAL {{
        ?class rdfs:subClassOf ?superClass .
        ?superClass rdfs:label ?superClassName .
      }}

      # Optionally retrieve the subclass name
      OPTIONAL {{
        ?subClass rdfs:subClassOf ?class .
        ?subClass rdfs:label ?subClassName .
      }}

      # Optionally retrieve the type of the class
      OPTIONAL {{
        GRAPH ?coco {{
          ?class rdf:type ?cocoid .
        }}
        ?cocoid rdfs:label ?type .
      }}

      # Exclude deprecated classes and superclasses
      FILTER (NOT EXISTS {{ ?class meta:valDeprecationDate ?xdt1 }})
      FILTER (NOT EXISTS {{ ?superClass meta:valDeprecationDate ?xdt2 }})
    }}
    ORDER BY ?uniqueName  # Order results by uniqueName for consistent pagination
    LIMIT {batch_size}    # Limit the number of results per batch
    """

    try:
        # Notify the start of query execution
        print(f"Executing query starting after '{last_unique_name}'")
        # Set the query and return format (CSV) for the SPARQL endpoint
        sparql.setQuery(query)
        sparql.setReturnFormat(CSV)

        # Execute the query and retrieve the results in CSV format
        results = sparql.query().convert()
        # Decode the CSV data from bytes to string
        csv_data = results.decode('utf-8')
        # Use StringIO to read the CSV data as a file
        csv_file = io.StringIO(csv_data)
        # Create a CSV DictReader to parse the CSV data
        csv_reader = csv.DictReader(csv_file)
        # Convert the CSV reader to a list of dictionaries (rows)
        rows = list(csv_reader)
        # Get the number of results retrieved in this batch
        num_results = len(rows)
        print(f"Retrieved {num_results} results")

        # Check if no results were returned, indicating the end of data
        if num_results == 0:
            more_data = False  # Set flag to False to exit the loop
            break

        # Process each result in the current batch
        for result in rows:
            # Extract and clean the uniqueName
            unique_name = result.get("uniqueName", "").strip()
            if not unique_name:
                continue  # Skip if unique_name is empty

            # Extract and clean other optional fields
            description = replace_html_entities(result.get("description", "").strip())
            super_class_name = result.get("superClassName", "").strip()
            type_name = result.get("type", "").strip()
            sub_class_name = result.get("subClassName", "").strip()

            # Initialize the data structure for the uniqueName if not already present
            if unique_name not in data:
                data[unique_name] = {
                    "superClasses": set(),    # Set to store unique superClass names
                    "subClasses": set(),      # Set to store unique subClass names
                    "description": description,  # Description of the class
                    "types": set()            # Set to store unique types
                }

            # Add the superClass name to the set if it exists
            if super_class_name:
                data[unique_name]["superClasses"].add(super_class_name)
            # Add the subClass name to the set if it exists
            if sub_class_name:
                data[unique_name]["subClasses"].add(sub_class_name)
            # Add the type to the set if it exists
            if type_name:
                data[unique_name]["types"].add(type_name)
            # Update the description if it's not already set
            if not data[unique_name]["description"] and description:
                data[unique_name]["description"] = description

        # Update the last_unique_name for the next batch using the last uniqueName in the current batch
        last_unique_name = rows[-1]["uniqueName"].strip()

    except Exception as e:
        # Print error message and stack trace if an exception occurs
        print(f"An error occurred after '{last_unique_name}': {e}")
        traceback.print_exc()
        # Optionally adjust batch size or implement retry logic here
        more_data = False  # Stop the loop on error

# After all batches are processed, print the total number of unique names collected
print(f"Finished processing all batches. Total unique names collected: {len(data)}")

# Step 1: Separate entries without superclasses, subclasses, description, and types
print("Filtering entries without superclasses, subclasses, description, and types...")
# Initialize lists to hold entries with and without attributes
entries_with_attributes = []
entries_without_attributes = []

# Iterate over each unique_name and its associated info
for unique_name, info in data.items():
    # Check if the entry has any of the specified attributes
    has_superclasses = len(info["superClasses"]) > 0
    has_subclasses = len(info["subClasses"]) > 0
    has_description = bool(info["description"])
    has_types = len(info["types"]) > 0

    # Create a dictionary for the entry with formatted data
    entry = {
        "uniqueName": unique_name,
        "superclasses": ", ".join(info["superClasses"]),  # Convert set to comma-separated string
        "subclasses": ", ".join(info["subClasses"]),      # Convert set to comma-separated string
        "description": info["description"],               # Use the description as it is
        "types": ", ".join(info["types"])                 # Convert set to comma-separated string
    }

    # If the entry has at least one attribute, add it to entries_with_attributes
    if has_superclasses or has_subclasses or has_description or has_types:
        entries_with_attributes.append(entry)
    else:
        # If the entry lacks all attributes, add it to entries_without_attributes
        entries_without_attributes.append(entry)

# Print the counts of entries with and without attributes
print(f"Entries with attributes: {len(entries_with_attributes)}")
print(f"Entries without attributes: {len(entries_without_attributes)}")

# Step 2: Write the entries with attributes to the main JSON file
print(f"Writing data to 'final_output.json'...")
with open("data/final_output.json", "w", encoding='utf-8') as json_file:
    # Dump the list of entries to the JSON file with indentation and UTF-8 encoding
    json.dump(entries_with_attributes, json_file, indent=4, ensure_ascii=False)
print("Data successfully written to 'final_output.json'")

# Step 3: Write the entries without attributes to a new JSON file
print(f"Writing data to 'filtered_out_data.json'...")
with open("data/filtered_out_data.json", "w", encoding='utf-8') as json_file:
    # Dump the list of entries to the JSON file with indentation and UTF-8 encoding
    json.dump(entries_without_attributes, json_file, indent=4, ensure_ascii=False)
print("Data successfully written to 'filtered_out_data.json'")
