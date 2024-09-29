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

     # Create a mapping from uniqueName to node data for quick access
    uniqueName_to_node = { item['uniqueName']: item for item in data }

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
    
    # Define functions to find parent and child nodes up to specified levels using mappings and visited sets
    def find_parents(node_name, level, visited=None):
        if visited is None:
            visited = set()
        # Base case: stop recursion if no more levels to traverse or node already
        if level == 0 or node_name in visited:
            return set()
        visited.add(node_name)
        parents = set()
        node = uniqueName_to_node.get(node_name)
        if not node:
            return parents
        superclasses = node.get('superclasses', '')
        superclasses_list = [s.strip() for s in superclasses.split(',') if s.strip()]
        for parent_name in superclasses_list:
            if parent_name in uniqueName_to_node:
                parents.add(parent_name)
                parents.update(find_parents(parent_name, level - 1, visited))
        return parents
    
    def find_children(node_name, level, visited=None):
        if visited is None:
            visited = set()
        # Base case: stop recursion if no more levels to traverse or node already
        if level == 0 or node_name in visited:
            return set()
        visited.add(node_name)
        children = set()
        node = uniqueName_to_node.get(node_name)
        if not node:
            return children
        subclasses = node.get('subclasses', '')
        subclasses_list = [s.strip() for s in subclasses.split(',') if s.strip()]
        for child_name in subclasses_list:
            if child_name in uniqueName_to_node:
                children.add(child_name)
                children.update(find_children(child_name, level - 1, visited))
        return children

    # Initialize PyVis network graph with white background and black text
    net = Network(height="82vh", width="100%", bgcolor="#ffffff", font_color="black", directed=True)

    # Filtering logic for displaying nodes up to specified parent and child levels from the search term
    if search_term and search_term in G:
        # Find parent and child nodes using the functions with mapping and visited sets
        parent_nodes = find_parents(search_term, parent_limit)
        child_nodes = find_children(search_term, children_limit)
        # Include the search_term in both sets
        parent_nodes.add(search_term)
        child_nodes.add(search_term)

        # Combine parent, child nodes, and the search term into one subgraph
        sub_graph_nodes = parent_nodes.union(child_nodes)
        sub_graph = G.subgraph(sub_graph_nodes).copy()

        # Convert subgraph to PyVis graph
        net.from_nx(sub_graph)

        for node in sub_graph_nodes:
            node_data = net.get_node(node)
            if node == search_term:
                node_data["color"] = "red"  # Searched node
            elif node in parent_nodes:
                node_data["color"] = "green"  # Parent nodes
            elif node in child_nodes:
                node_data["color"] = "blue"  # Child nodes
            else:
                node_data["color"] = "white"  # Default color for other nodes

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
        <div id="networkx-container">
            {graph_html}  <!-- Embed PyVis graph -->
        </div>
        
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
            <button id="fullscreen-btn" onclick="toggleFullscreen()" style="
                padding: 10px 20px; 
                font-size: 16px; 
                background: linear-gradient(90deg, #87CEEB 0%, #FFD700 100%);  /* Gradient from light blue to yellow */
                color: white;  /* Text color */
                border: 3px solid #002855;  /* Navy blue border */
                border-radius: 5px; 
                cursor: pointer; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                Go Fullscreen
            </button>
        </div>

        <script>
            function toggleFullscreen() {{
                const elem = document.getElementById('networkx-container');
                if (!document.fullscreenElement) {{
                    elem.style.backgroundColor = "white";  // Set background color to white in fullscreen
                    elem.requestFullscreen().catch(err => {{
                        alert(`Error attempting to enable full-screen mode: ${{err.message}} (${{err.name}})`);
                    }});
                }} else {{
                    document.exitFullscreen();
                }}
            }}
        </script>
        
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
