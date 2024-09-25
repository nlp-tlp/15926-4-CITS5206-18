import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import json
from networkx.readwrite import json_graph
import streamlit.components.v1 as components

def display_networkx_plot(data, search_term, parent_limit, children_limit):
    """Display the NetworkX plot with user-defined parameters."""
    
    # Header for the NetworkX Plot section
    st.header("Network Plot")

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges with descriptions
    for item in data:
        unique_name = item['uniqueName']
        superclasses = item['superclasses'].split(', ') if 'superclasses' in item and item['superclasses'] else []
        subclasses = item['subclasses'].split(', ') if 'subclasses' in item and item['subclasses'] else []
        description = str(item['description']) if 'description' in item and item['description'] else ""
        types = str(item['types']) if 'types' in item and item['types'] else ""

        # Add node to the graph with description as tooltip
        G.add_node(unique_name, title=description)

        # Add node types to the graph node
        G.add_node(unique_name, types = types)

        # Add edges for superclasses and subclasses
        for superclass in superclasses:
            if superclass:
                G.add_node(superclass)
                G.add_edge(superclass, unique_name)  # Correct direction: node to superclass

        for subclass in subclasses:
            if subclass:
                G.add_node(subclass)
                G.add_edge(unique_name, subclass)  # Correct direction: subclass to node

    # Initialize PyVis network graph with white background and black text
    net = Network(height="82vh", width="100%", bgcolor="#ffffff", font_color="black", directed=True)

    # Filtering logic for displaying nodes up to specified parent and child levels from the search term
    if search_term and search_term in G:
        # BFS for Parent Nodes up to the specified parent levels
        parent_nodes = {search_term}
        current_level_nodes = {search_term}

        for _ in range(parent_limit):
            next_level_nodes = set()
            for node in current_level_nodes:
                next_level_nodes.update(G.predecessors(node))  # Parents (ancestors)
            current_level_nodes = next_level_nodes - parent_nodes
            parent_nodes.update(current_level_nodes)

        # BFS for Child Nodes up to the specified children levels
        child_nodes = {search_term}
        current_level_nodes = {search_term}

        for _ in range(children_limit):
            next_level_nodes = set()
            for node in current_level_nodes:
                next_level_nodes.update(G.successors(node))  # Children (descendants)
            current_level_nodes = next_level_nodes - child_nodes
            child_nodes.update(current_level_nodes)

        # Combine parent, child nodes, and the search term into one subgraph
        sub_graph_nodes = parent_nodes.union(child_nodes)
        sub_graph = G.subgraph(sub_graph_nodes).copy()

        # Convert subgraph to PyVis graph
        net.from_nx(sub_graph)

        # Apply specific colors based on node type
        for node in sub_graph.nodes():
            if node == search_term:
                net.get_node(node)["color"] = "red"  # Searched node
            elif node in parent_nodes:
                net.get_node(node)["color"] = "green"  # Parent nodes
            elif node in child_nodes:
                net.get_node(node)["color"] = "blue"  # Child nodes
            else:
                net.get_node(node)["color"] = "white"  # Default color for other nodes

    else:
        # If no search term or term not found, visualize entire graph
        net.from_nx(G)

    # Save and embed the PyVis graph
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        tmp_file.seek(0)
        graph_html = tmp_file.read().decode()

    # Convert graph to JSON for JavaScript interactions
    graph_data = json_graph.node_link_data(G)
    graph_json = json.dumps(graph_data)

    # JavaScript for handling node clicks in NetworkX Plot
    components.html(f"""
        {graph_html}  <!-- Embed PyVis graph -->
        <script type="text/javascript">
            const graphData = {graph_json};  // Safely pass JSON data

            // Function to escape HTML content in node description
            function escapeHtml(content) {{
                const div = document.createElement('div');
                div.textContent = content;
                return div.innerHTML;
            }}

            // Function to handle node clicks
            function nodeClick(nodeId) {{
                const node = graphData.nodes.find(n => n.id === nodeId);
                const nodeTitle = node.title;
                const floatingBar = window.parent.document.getElementById('sidebarFloatingBar');
                floatingBar.innerHTML = nodeTitle ? escapeHtml(nodeTitle) : "No description available.";
                floatingBar.style.display = 'block';

                // To display node types information
                const nodetypes = node.types;
                const nodeType = window.parent.document.getElementById('nodeType');
                nodeType.innerHTML = nodetypes ? escapeHtml(nodetypes) : "No Information available.";
                nodeType.style.display = 'block';
            }}

            // Access the network instance and set up click event
            var network = window.network;
            network.on("click", function(params) {{
                if (params.nodes.length > 0) {{
                    var nodeId = params.nodes[0];
                    nodeClick(nodeId);
                }}
            }});
        </script>
    """, height=820)
