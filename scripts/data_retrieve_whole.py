import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import os

# Function to replace HTML entities in descriptions
def replace_html_entities(text):
    return text.replace('&lt;', '<').replace('&gt;', '>')

# Define SPARQL endpoint
sparql = SPARQLWrapper("http://190.92.134.58:8890/sparql")

# List of prefixes to divide the queries
prefixes = [chr(i) for i in range(ord('A'), ord('Z')+1)]  # A-Z

# Dictionary to hold the combined results
data = {}

# Step 1: Query each subset of classes
for prefix in prefixes:
    query = f"""
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix meta: <http://data.15926.org/meta/>
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?uniqueName ?superClassName ?description ?type ?subClassName
    WHERE {{
      ?class rdfs:label ?uniqueName .
      FILTER (STRSTARTS(STR(?uniqueName), "{prefix}"))

      OPTIONAL {{
        ?class skos:definition ?description .
      }}

      OPTIONAL {{
        ?class rdfs:subClassOf ?superClass .
        ?superClass rdfs:label ?superClassName .
      }}

      OPTIONAL {{
        ?subClass rdfs:subClassOf ?class .
        ?subClass rdfs:label ?subClassName .
      }}

      OPTIONAL {{
        GRAPH ?coco {{
          ?class rdf:type ?cocoid .
        }}
        ?cocoid rdfs:label ?type .
      }}

      FILTER (NOT EXISTS {{ ?class meta:valDeprecationDate ?xdt1 }})
      FILTER (NOT EXISTS {{ ?superClass meta:valDeprecationDate ?xdt2 }})
    }}
    ORDER BY ?uniqueName
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    # Process the results
    for result in results["results"]["bindings"]:
        unique_name = result["uniqueName"]["value"]
        description = replace_html_entities(result.get("description", {}).get("value", ""))
        super_class_name = result.get("superClassName", {}).get("value", "")
        type_name = result.get("type", {}).get("value", "")
        sub_class_name = result.get("subClassName", {}).get("value", "")
        
        if unique_name not in data:
            data[unique_name] = {
                "superClasses": set(),
                "subClasses": set(),
                "description": description,
                "types": set()
            }
        
        if super_class_name:
            data[unique_name]["superClasses"].add(super_class_name)
        
        if sub_class_name:
            data[unique_name]["subClasses"].add(sub_class_name)
        
        if type_name:
            data[unique_name]["types"].add(type_name)

# Step 2: Prepare the data for output
output_data = []
for unique_name, info in data.items():
    output_data.append({
        "uniqueName": unique_name,
        "superclasses": ", ".join(info["superClasses"]),
        "subclasses": ", ".join(info["subClasses"]),
        "description": info["description"],
        "types": ", ".join(info["types"])
    })

# Convert the processed data to CSV
output_df = pd.DataFrame(output_data)
output_df.to_csv("final_output.csv", index=False)

# JSON output:
with open("final_output.json", "w") as json_file:
    json.dump(output_data, json_file, indent=4)
