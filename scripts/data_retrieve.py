import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import json

# Function to replace HTML entities like &lt; and &gt; with < and >
def replace_html_entities(text):
    return text.replace('&lt;', '<').replace('&gt;', '>')

# Define the SPARQL endpoint where queries will be sent
sparql = SPARQLWrapper("http://190.92.134.58:8890/sparql")

# List of prefixes to divide the queries (A-Z and 0-9), which allows querying in subsets
prefixes = [chr(i) for i in range(ord('A'), ord('Z')+1)] + [str(i) for i in range(0, 10)]  # A-Z and 0-9

# List of uniqueNames to filter out (these names can't be searched)
excluded_unique_names = [
    "AllDifferent", "AnnotationProperty", "DataRange", "DatatypeProperty",
    "DeprecatedClass", "DeprecatedProperty", "FunctionalProperty",
    "Ontology", "OntologyProperty"
]

# Dictionary to hold the combined results from all queries
data = {}

# Step 1: Query each subset of classes based on the prefix
for prefix in prefixes:
    # SPARQL query is constructed here for each prefix
    query = f"""
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>   # Standard RDF schema prefix for class relationships
    prefix skos: <http://www.w3.org/2004/02/skos/core#>    # SKOS (Simple Knowledge Organization System) prefix for definitions
    prefix meta: <http://data.15926.org/meta/>             # Custom meta-data namespace for deprecation and other info
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  # Basic RDF syntax

    SELECT ?uniqueName ?superClassName ?description ?type ?subClassName
    WHERE {{
      # Retrieve the label (name) of the class and bind it to ?uniqueName
      ?class rdfs:label ?uniqueName .
      
      # Filter the results to only include classes where the name starts with the current prefix (A-Z or 0-9)
      FILTER (STRSTARTS(STR(?uniqueName), "{prefix}"))
      
      # Exclude any classes whose names match those in the excluded list (e.g., AllDifferent, AnnotationProperty, etc.)
      FILTER (?uniqueName NOT IN ({', '.join([f'"{name}"' for name in excluded_unique_names])}))

      # Optionally retrieve the definition of the class from SKOS (if it exists)
      OPTIONAL {{
        ?class skos:definition ?description .
      }}

      # Optionally retrieve the superclass of the class, if it has one
      OPTIONAL {{
        ?class rdfs:subClassOf ?superClass .
        ?superClass rdfs:label ?superClassName .
      }}

      # Optionally retrieve any subclasses of the class, if they exist
      OPTIONAL {{
        ?subClass rdfs:subClassOf ?class .
        ?subClass rdfs:label ?subClassName .
      }}

      # Optionally retrieve the type of the class if it is defined
      OPTIONAL {{
        GRAPH ?coco {{
          ?class rdf:type ?cocoid .
        }}
        ?cocoid rdfs:label ?type .
      }}

      # Filter out any classes that have been marked as deprecated (using meta:valDeprecationDate)
      FILTER (NOT EXISTS {{ ?class meta:valDeprecationDate ?xdt1 }})
      FILTER (NOT EXISTS {{ ?superClass meta:valDeprecationDate ?xdt2 }})
    }}
    ORDER BY ?uniqueName   # Order the results by the uniqueName
    """
    
    # Set the query to the SPARQL endpoint and set the return format to JSON
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results in JSON format
    results = sparql.query().convert()
    
    # Process the results to extract useful information
    for result in results["results"]["bindings"]:
        # Get the uniqueName (label) of the class
        unique_name = result["uniqueName"]["value"]
        
        # Get the description, if available
        description = replace_html_entities(result.get("description", {}).get("value", ""))
        
        # Get the superClass name, if available
        super_class_name = result.get("superClassName", {}).get("value", "")
        
        # Get the type, if available
        type_name = result.get("type", {}).get("value", "")
        
        # Get the subClass name, if available
        sub_class_name = result.get("subClassName", {}).get("value", "")
        
        # Initialize data for the uniqueName if it hasn't been added yet
        if unique_name not in data:
            data[unique_name] = {
                "superClasses": set(),  # Set to store unique superClass names
                "subClasses": set(),    # Set to store unique subClass names
                "description": description,  # The description of the class
                "types": set()          # Set to store unique types
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

# Step 2: Prepare the data for output
output_data = []

# Format the data for each uniqueName into a structured output format
for unique_name, info in data.items():
    output_data.append({
        "uniqueName": unique_name,
        "superclasses": ", ".join(info["superClasses"]),    # Convert set to comma-separated string
        "subclasses": ", ".join(info["subClasses"]),        # Convert set to comma-separated string
        "description": info["description"],                # Use the description as it is
        "types": ", ".join(info["types"])                  # Convert set to comma-separated string
    })

# Convert the processed data to CSV if needed (commented out for now)
# output_df = pd.DataFrame(output_data)
# output_df.to_csv("../data/final_output.csv", index=False)

# Write the output data to a JSON file
with open("../data/final_output.json", "w") as json_file:
    json.dump(output_data, json_file, indent=4)
