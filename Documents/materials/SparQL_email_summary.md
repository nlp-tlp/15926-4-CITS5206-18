# Emails about SPARQL

---

# SPARQL Email Summary

Melinda Hodkiewicz requested assistance with writing a SPARQL query to download all classes from the current ISO 15926-4 Reference Data Library (RDL). She sought clarification on what to write in the "Default Data Set Name (Graph IRI)" box and verification if her basic SPARQL query was correct.

### Onno Paap's Response

1. **SPARQL Endpoint Information**:
   - **Endpoint URL**: The RDL database runs on Virtuoso Open Source. Use the following SPARQL endpoint URL: `http://190.92.134.58:8890/sparql`.
2. **Identifying Named Graphs**:
   - **Trick to Identify Graphs**: By making a deliberate mistake in the endpoint URL (`https://data.15926.org/abcd`), the reverse proxy will show the correct named graphs to use.
   - **Named Graphs List**:
     - `http://data.15926.org/rdl` - ISO 15926 Reference Data Library
     - `http://data.15926.org/dm` - ISO 15926-2 Data Model
     - `http://data.15926.org/lci` - Extended Data Model
     - `http://data.15926.org/meta` - Meta data
     - `http://data.15926.org/all` - All endpoints
     - Additional graphs for various standards and templates (e.g., `http://data.15926.org/tpl`, `http://data.15926.org/coco`).
3. **Detailed SPARQL Query Example**:
   - **Query**:
     ```sql
     prefix meta: <http://data.15926.org/meta/>

     select ?classname ?parentclassname ?spreadsheetname

     {graph <http://data.15926.org/rdl>{

     ?id rdfs:label ?classname.

     filter (not exists {?id meta:valDeprecationDate ?xdt1})

     ?id rdfs:subClassOf ?parentid.

     ?parentid rdfs:label ?parentclassname.

     filter (not exists {?parentid meta:valDeprecationDate ?xdt2})

     {graph ?coco{?id rdf:type ?cocoid}}

     ?cocoid rdfs:label ?spreadsheetname.

     }} order by ?classname

     ```
   - **Explanation**:
     - This query retrieves class names, parent class names, and associated spreadsheet names.
     - It excludes deprecated classes by applying filters on `meta:valDeprecationDate`.
4. **Query Output and Formatting**:
   - **Line Limit**: The SPARQL output is limited to 10,000 lines, but this can be increased to 100,000 if needed.
   - **Output Format**: Use CSV format for the output, as it is more convenient than the "Spreadsheet" option.
5. **Additional Notes**:
   - **Provenance Metadata**: The first named graphs are metadata and connect additional data to the `/rdl` named graph.
   - **Prefix Statements**: Virtuoso has some prefix statements prepared, so you don’t have to define them for `rdf:` and `rdfs:` in your queries.
   - **Deprecated Classes**: Be cautious with deleted classes, which have a `meta:valDeprecationDate` predicate.

### Steps to Get Data According to This Email

1. **Access the SPARQL Endpoint**:
   Open your web browser and navigate to the Virtuoso SPARQL query interface at `http://190.92.134.58:8890/sparql`.
2. **Enter the SPARQL Query**:
   Copy and paste the SPARQL query mentioned before into the query editor on the SPARQL endpoint page.
3. **Execute the Query**:
   Click the "Run" or "Execute" button to run the query.
4. **Download the Results**:
   Once the query completes, you can choose to download the results in CSV format.

I’ve attached the data file to the link below.

[https://drive.google.com/file/d/1AvH_pJmZTkkhDut_K35N6b2U98kDa6yu/view?usp=sharing](https://drive.google.com/file/d/1AvH_pJmZTkkhDut_K35N6b2U98kDa6yu/view?usp=sharing)

---
