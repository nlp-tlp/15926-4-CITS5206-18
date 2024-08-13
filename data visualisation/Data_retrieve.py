import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

# Define SPARQL endpoint and query
sparql = SPARQLWrapper("http://190.92.134.58:8890/sparql")
sparql.setQuery("""
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix meta: <http://data.15926.org/meta/>

    SELECT ?uniqueName ?description ?childClassName ?childDescription ?childSuperClasses ?childSuperClassDescription
    WHERE {
      ?class rdfs:subClassOf <http://data.15926.org/lci/FunctionalObject> .
      ?class rdfs:label ?uniqueName .

      OPTIONAL {
        ?class skos:definition ?description .
      }

      OPTIONAL {
        ?childClass rdfs:subClassOf ?class .
        ?childClass rdfs:label ?childClassName .
        FILTER (NOT EXISTS {?childClass meta:valDeprecationDate ?xdt2})

        OPTIONAL {
          ?childClass skos:definition ?childDescription .
        }

        OPTIONAL {
          ?childSuperClass rdfs:subClassOf ?childClass .
          ?childSuperClass rdfs:label ?childSuperClasses .
          FILTER (NOT EXISTS {?childSuperClass meta:valDeprecationDate ?xdt3})

          OPTIONAL {
            ?childSuperClass skos:definition ?childSuperClassDescription .
          }
        }
      }
    }
    ORDER BY ?uniqueName ?childClassName
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Process the results into a dictionary
data = {}

for result in results["results"]["bindings"]:
    unique_name = result["uniqueName"]["value"]
    description = result.get("description", {}).get("value", "")
    
    child_class = result.get("childClassName", {}).get("value", "")
    child_description = result.get("childDescription", {}).get("value", "")
    
    child_super_classes = result.get("childSuperClasses", {}).get("value", "")
    child_superclass_description = result.get("childSuperClassDescription", {}).get("value", "")

    # Initialize unique_name in data if not already present
    if unique_name not in data:
        data[unique_name] = {
            "Super Classes": set(),
            "Sub Classes": set(),
            "Description": description
        }

    # Add child classes to unique_name's subclasses
    if child_class:
        data[unique_name]["Sub Classes"].add(child_class)
        
        # Initialize the child class entry
        if child_class not in data:
            data[child_class] = {
                "Super Classes": set(),
                "Sub Classes": set(),
                "Description": child_description
            }
        
        # Add unique_name as a superclass of the child class
        data[child_class]["Super Classes"].add(unique_name)
        
        # Handle the superclasses of the child class
        if child_super_classes:
            data[child_class]["Sub Classes"].add(child_super_classes)
            
            # Initialize the superclass entry
            if child_super_classes not in data:
                data[child_super_classes] = {
                    "Super Classes": set(),
                    "Sub Classes": set(),
                    "Description": child_superclass_description
                }
            
            # Add child_class as a superclass of child_super_classes
            data[child_super_classes]["Super Classes"].add(child_class)

# Prepare the data for CSV output
output_data = []
for unique_name, info in data.items():
    output_data.append({
        "uniqueName": unique_name,
        "superclasses": ", ".join(info["Super Classes"]),
        "subclasses": ", ".join(info["Sub Classes"]),
        "description": info["Description"]
    })

# Convert the processed data into a DataFrame
df = pd.DataFrame(output_data)

# Save to CSV
df.to_csv("final_output.csv", index=False)


