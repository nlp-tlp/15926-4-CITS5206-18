import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

# Load the new dataset
data = pd.read_csv('Functional Database 2-level.csv')

# Create the sidebar for search bars
st.sidebar.header("Search Options")

# First search bar: Search by unique name
search_term = st.sidebar.text_input("Search by Unique Name")

# Second search bar: Number of parent nodes to display
parent_limit = st.sidebar.number_input("Number of Parent Nodes", min_value=0, max_value=10, value=3, step=1)

# Third search bar: Number of children nodes to display
children_limit = st.sidebar.number_input("Number of Children Nodes", min_value=0, max_value=10, value=3, step=1)

# Create a graph
G = nx.DiGraph()

# Add nodes and edges, including the description in the node's title (which is shown as a tooltip)
for index, row in data.iterrows():
    unique_name = row['uniqueName']
    
    # Handle potential NaN values in the superclasses and subclasses columns
    superclasses = row['superclasses']
    if isinstance(superclasses, str):
        superclasses = superclasses.split(', ')
    else:
        superclasses = []
    
    subclasses = row['subclasses']
    if isinstance(subclasses, str):
        subclasses = subclasses.split(', ')
    else:
        subclasses = []

    # Ensure description is always a string
    description = str(row['description']) if not pd.isna(row['description']) else ""

    # Add node to the graph with the description as a tooltip
    G.add_node(unique_name, title=description)  
    
    # Add edges for superclasses
    for superclass in superclasses:
        if superclass:
            G.add_node(superclass)
            G.add_edge(superclass, unique_name)
    
    # Add edges for subclasses
    for subclass in subclasses:
        if subclass:
            G.add_node(subclass)
            G.add_edge(unique_name, subclass)

# Initialize the network graph visualization
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)

# Filter the graph if a search term is provided
if search_term and search_term in G:
    # Get parent nodes (ancestors) up to the specified limit
    parent_nodes = list(nx.ancestors(G, search_term))[:parent_limit]
    
    # Get child nodes (descendants) up to the specified limit
    child_nodes = list(nx.descendants(G, search_term))[:children_limit]

    # Include neighbors (directly connected nodes)
    neighbors = list(G.neighbors(search_term))

    # Create a subgraph with the selected node, its parents, and its children
    sub_graph = G.subgraph([search_term] + parent_nodes + child_nodes + neighbors).copy()

    # Set positions manually to place the searched node on top,
    # parent nodes below it, and children at the bottom
    pos = {}
    pos[search_term] = (0, 0)  # Top node

    # Set positions for parent nodes below the searched node
    for i, parent in enumerate(parent_nodes):
        pos[parent] = (0, -(i + 1))

    # Set positions for child nodes at the bottom
    for i, child in enumerate(child_nodes):
        pos[child] = (0, -(len(parent_nodes) + i + 1))

    # Generate network graph visualization with custom positions
    net.from_nx(sub_graph)

    # Apply the positions and set custom colors
    for node, (x, y) in pos.items():
        net.get_node(node)["x"] = x * 100
        net.get_node(node)["y"] = y * -100  # Negative Y to place below the center

        # Set custom colors
        if node == search_term:
            net.get_node(node)["color"] = "red"  # Color for searched node
        elif node in parent_nodes:
            net.get_node(node)["color"] = "green"  # Color for parent nodes
        elif node in child_nodes:
            net.get_node(node)["color"] = "blue"  # Color for child nodes

else:
    # If no search term is provided or the search term is not found, visualize the entire graph
    net.from_nx(G)

# Adjust the height of the description box to accommodate the full text
for node in net.nodes:
    if 'title' in node:
        node["title"] = f"{node['title']}"

# Use a temporary file to avoid file write issues
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    net.save_graph(tmp_file.name)
    tmp_file.seek(0)
    components.html(tmp_file.read().decode(), height=750)
