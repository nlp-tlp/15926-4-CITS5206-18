import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import json

# Function to replace HTML entities like &lt; and &gt; with < and >
def replace_html_entities(text):
    return text.replace('&lt;', '<').replace('&gt;', '>')

# Start of the script
print("Starting data extraction...")

# Define the SPARQL endpoint where queries will be sent
sparql = SPARQLWrapper("http://190.92.134.58:8890/sparql")

# Dictionary to hold the combined results from all queries
data = {}
# Dictionary to hold the filtered out data for classes with no superclass, subclass, description, or type
filtered_out_data = {}

# Initialize pagination variables
batch_size = 5000  # Adjust as needed based on endpoint limitations
last_unique_name = ""  # For keyset pagination
more_data = True  # Control variable for the pagination loop

# Step 1: Query using pagination
while more_data:
    # Build the pagination filter based on the last uniqueName retrieved
    if last_unique_name:
        pagination_filter = f'FILTER (STR(?uniqueName) > "{last_unique_name}")'
    else:
        pagination_filter = ''  # No filter for the first batch

    # Construct the SPARQL query with the pagination filter
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   # Standard RDF schema prefix for class relationships
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>    # SKOS prefix for definitions
    PREFIX meta: <http://data.15926.org/meta/>             # Custom meta-data namespace
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  # Basic RDF syntax

    SELECT ?uniqueName ?superClassName ?description ?type ?subClassName
    WHERE {{
      # Retrieve the label (uniqueName) of the class
      ?class rdfs:label ?uniqueName .
      
      {pagination_filter}  # Apply pagination filter if not the first batch
      
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

      # Filter out any classes that have been marked as deprecated
      FILTER (NOT EXISTS {{ ?class meta:valDeprecationDate ?xdt1 }})
      FILTER (NOT EXISTS {{ ?superClass meta:valDeprecationDate ?xdt2 }})
    }}
    ORDER BY ?uniqueName   # Order the results by uniqueName for consistent pagination
    LIMIT {batch_size}
    """

    # Print progress information
    print(f"Processing batch starting after '{last_unique_name}'")
    print("Executing query...")

    # Set the query to the SPARQL endpoint and set the return format to JSON
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results in JSON format
    results = sparql.query().convert()
    
    # Extract the bindings (results) from the query response
    bindings = results["results"]["bindings"]
    num_results = len(bindings)
    print(f"Retrieved {num_results} results")

    # If no results are returned, we've reached the end of the data
    if not bindings:
        print("No more data to process.")
        more_data = False
        break

    # Process each result in the current batch
    for result in bindings:
        # Get the uniqueName (label) of the class
        unique_name = result["uniqueName"]["value"]
        
        # Update last_unique_name for the next batch
        last_unique_name = unique_name
        
        # Get the description, if available
        description = replace_html_entities(result.get("description", {}).get("value", ""))
        
        # Get the superClass name, if available
        super_class_name = result.get("superClassName", {}).get("value", "")
        
        # Get the type, if available
        type_name = result.get("type", {}).get("value", "")
        
        # Get the subClass name, if available
        sub_class_name = result.get("subClassName", {}).get("value", "")

        # Check if the class lacks all relevant data
        if not super_class_name and not sub_class_name and not description and not type_name:
            # Add to filtered_out_data and skip adding to main data
            filtered_out_data[unique_name] = {
                "uniqueName": unique_name,
                "superclasses": super_class_name,
                "subclasses": sub_class_name,
                "description": description,
                "types": type_name
            }
            continue  # Skip to the next result
        
        # Initialize data for the uniqueName if it hasn't been added yet
        if unique_name not in data:
            data[unique_name] = {
                "uniqueName": unique_name,
                "superClasses": set(),    # Set to store unique superClass names
                "subClasses": set(),      # Set to store unique subClass names
                "description": description,  # The description of the class
                "types": set()            # Set to store unique types
            }
        
        # Add the superClass name to the set (if it exists)
        if super_class_name:
            data[unique_name]["superClasses"].add(super_class_name)
        
        # Add the subClass name to the set (if it exists)
        if sub_class_name:
            data[unique_name]["subClasses"].add(sub_class_name)
        
        # Add the type to the set (if it exists)
        if type_name:
            data[unique_name]["types"].add(type_name)

    print(f"Processed batch ending with '{last_unique_name}'")

# Step 2: Prepare the data for output
print("Preparing data for output...")

# Convert the data dictionary to a list for sorting
output_data = list(data.values())

# Sort the output_data list alphabetically by 'uniqueName'
# All entries starting with letters are listed first in alphabetical order.
# Entries starting with numbers are listed after, also in numerical/alphabetical order.
output_data.sort(key=lambda x: (
    x["uniqueName"][0].isspace() or not x["uniqueName"][0].isalnum(),  # Special characters or blanks come last
    x["uniqueName"][0].isdigit(),  # Numbers come after letters
    x["uniqueName"].lower()  # Case-insensitive alphabetical sorting
))


# Prepare filtered-out data for writing and sort it
filtered_out_list = list(filtered_out_data.values())
filtered_out_list.sort(key=lambda x: (
    x["uniqueName"][0].isspace() or not x["uniqueName"][0].isalnum(),
    x["uniqueName"][0].isdigit(),
    x["uniqueName"].lower()
))


# Display the total counts
total_entries = len(data) + len(filtered_out_data)
print(f"Total number of entries collected: {total_entries}")
print(f"Number of entries with attributes: {len(output_data)}")
print(f"Number of entries without attributes: {len(filtered_out_list)}")

# Format the data entries for output
for entry in output_data:
    entry["superclasses"] = ", ".join(entry["superClasses"])
    entry["subclasses"] = ", ".join(entry["subClasses"])
    entry["types"] = ", ".join(entry["types"])
    # Remove the set data structures as they are no longer needed
    del entry["superClasses"]
    del entry["subClasses"]

# Write the main output data to a JSON file
print("Writing main output data to 'final_output.json'...")
with open("data/final_output.json", "w", encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=4, ensure_ascii=False)

# Write the filtered-out data to a separate JSON file
print("Writing filtered-out data to 'filtered_out_data.json'...")
with open("data/filtered_out_data.json", "w", encoding='utf-8') as filtered_file:
    json.dump(filtered_out_list, filtered_file, indent=4, ensure_ascii=False)

print("Files successfully saved.")
print("Data extraction completed successfully.")


