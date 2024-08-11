import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

# Load the dataset
data = pd.read_csv('final_rotating_equipment_data.csv')

# Create the sidebar for search bars
st.sidebar.header("Search Options")

# First search bar: Search by unique name
search_term = st.sidebar.text_input("Search by Unique Name")

# Second search bar: Number of parent nodes to display
parent_limit = st.sidebar.number_input("Number of Parent Nodes", min_value=0, max_value=10, value=3, step=1)

# Third search bar: Number of children nodes to display
children_limit = st.sidebar.number_input("Number of Children Nodes", min_value=0, max_value=10, value=3, step=1)

# Create a graph
G = nx.Graph()

# Add nodes and edges, including the TextDefinition in the node's title (which is shown as a tooltip)
for index, row in data.iterrows():
    unique_name = row['UniqueName']
    superclasses = row['SuperClass'].split(', ')
    text_definition = row['TextDefinition']
    
    # Add node to the graph with the TextDefinition as a tooltip
    G.add_node(unique_name, title=text_definition)  
    
    # Add edges for superclasses
    for superclass in superclasses:
        if superclass:
            G.add_node(superclass)
            G.add_edge(unique_name, superclass)

# Filter the graph if search term is provided
if search_term:
    if search_term in G:
        # Get parent nodes (ancestors) up to the specified limit
        parent_nodes = list(nx.ancestors(G, search_term))[:parent_limit]
        
        # Get child nodes (descendants) up to the specified limit
        child_nodes = list(nx.descendants(G, search_term))[:children_limit]

        # Include neighbors (directly connected nodes)
        neighbors = list(G.neighbors(search_term))

        # Create a subgraph with the selected node, its parents, and its children
        sub_graph = G.subgraph([search_term] + parent_nodes + child_nodes + neighbors).copy()
    else:
        sub_graph = nx.Graph()  # Empty graph if no match
else:
    sub_graph = G

# Generate network graph visualization
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
net.from_nx(sub_graph)

# Use a temporary file to avoid file write issues
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    net.save_graph(tmp_file.name)
    tmp_file.seek(0)
    components.html(tmp_file.read().decode(), height=750)
