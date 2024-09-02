import streamlit as st
import json
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import tempfile
from networkx.readwrite import json_graph

# Set the page layout to wide
st.set_page_config(layout="wide")

# Load custom CSS from an external file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("./style.css")

# Add the footer with copyright information
st.markdown(
    """
    <div class="footer" style="text-align: right; padding-right: 160px;">
        &copy;2024 , Made For <b>"UWA NLP-TLP Group"</b>, Designed and Developed by <b>Manish Varada Reddy, Melo Xue, Shanmugapriya Sankarraj, Xudong Ying, Yu Xia, Zihan Zhang<b>.
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state for page selection
if 'page' not in st.session_state:
    st.session_state.page = "D3.js Plot"  # Default page

# Add custom CSS for the sidebar logo and buttons
st.markdown(
    """
    <style>
    <div class="sidebar-logo">
        <img src="https://your-logo-url.com/logo.png" alt="Logo">
    </div>
    </style>
    """,
    unsafe_allow_html=True
)

# Add the logo to the sidebar using st.image
st.sidebar.image("nlp-tlp-logo.png", width=130)

# Create a sidebar header
st.sidebar.header("Navigation")

# Create two buttons in the sidebar
if st.sidebar.button("D3.js Plot"):
    st.session_state.page = "D3.js Plot"

if st.sidebar.button("NetworkX Plot"):
    st.session_state.page = "NetworkX Plot"

# Display content based on the selected page
if st.session_state.page == "NetworkX Plot":
    # NetworkX plot code:

    # Load the dataset from JSON file
    with open('final_output.json') as json_file:
        data = json.load(json_file)

    # Create the sidebar for search bars
    st.sidebar.header("Search Options")

    # Extract unique names
    unique_names = [item['uniqueName'] for item in data]

    # First search bar: Search by unique name with auto-fill
    search_term = st.sidebar.selectbox("Search by Unique Name", unique_names)

    # Input for the number of parent levels to display
    parent_level_limit = st.sidebar.number_input("Number of Parent Levels", min_value=0, max_value=10, value=3, step=1)

    # Input for the number of children levels to display
    children_level_limit = st.sidebar.number_input("Number of Children Levels", min_value=0, max_value=10, value=3, step=1)

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges with descriptions
    for item in data:
        unique_name = item['uniqueName']
        superclasses = item['superclasses'].split(', ') if 'superclasses' in item and item['superclasses'] else []
        subclasses = item['subclasses'].split(', ') if 'subclasses' in item and item['subclasses'] else []
        description = str(item['description']) if 'description' in item and item['description'] else ""

        # Add node to the graph with description as tooltip
        G.add_node(unique_name, title=description)

        # Add edges for superclasses and subclasses
        for superclass in superclasses:
            if superclass:
                G.add_node(superclass)
                G.add_edge(superclass, unique_name)  # Correct direction: superclass to the node

        for subclass in subclasses:
            if subclass:
                G.add_node(subclass)
                G.add_edge(unique_name, subclass)  # Correct direction: node to subclass

    # Initialize PyVis network graph with white background and black text
    net = Network(height="1000px", width="100%", bgcolor="white", font_color="black", directed=True)

    # Filtering logic for displaying nodes up to specified parent and child levels from the search term
    if search_term and search_term in G:
        # BFS for Parent Nodes up to the specified parent levels
        parent_nodes = {search_term}
        current_level_nodes = {search_term}

        for _ in range(parent_level_limit):
            next_level_nodes = set()
            for node in current_level_nodes:
                next_level_nodes.update(G.predecessors(node))  # Parents (ancestors)
            current_level_nodes = next_level_nodes - parent_nodes
            parent_nodes.update(current_level_nodes)

        # BFS for Child Nodes up to the specified children levels
        child_nodes = {search_term}
        current_level_nodes = {search_term}

        for _ in range(children_level_limit):
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

    # Sidebar for displaying node descriptions
    with st.sidebar:
        st.markdown("""
            <div id="sidebarFloatingBar" style="
                background-color: #fff;
                color: black;
                padding: 10px;
                border-radius: 5px;
                display: none;">
            </div>
            """, unsafe_allow_html=True)

    # JavaScript for handling node clicks
    components.html(f"""
        {graph_html}  <!-- Embed PyVis graph -->
        <script type="text/javascript">
            const graphData = {graph_json};  // Safely pass JSON data

            // Function to escape HTML content
            function escapeHtml(content) {{
                const div = document.createElement('div');
                div.textContent = content;
                return div.innerHTML;
            }}

            // Function to handle node clicks
            function nodeClick(nodeId) {{
                const node = graphData.nodes.find(n => n.id === nodeId);
                const nodeTitle = node && node.title ? node.title : nodeId;
                const floatingBar = window.parent.document.getElementById('sidebarFloatingBar');
                floatingBar.innerHTML = escapeHtml(nodeTitle);
                floatingBar.style.display = 'block';
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
    """, height=1000)



    st.header("NetworkX Plot")

elif st.session_state.page == "D3.js Plot":
    # D3.js plot code:

    # Load JSON data
    with open('final_output.json') as json_file:
        data = json.load(json_file)

    # Create the sidebar for search bars
    st.sidebar.header("Search Options")

    # Extract unique names
    unique_names = [item["uniqueName"] for item in data]

    # First search bar: Search by unique name with auto-fill
    search_term = st.sidebar.selectbox("Search by Unique Name", unique_names)

    # Second search bar: Number of parent levels to display
    parent_limit = st.sidebar.number_input("Number of Parent Levels", min_value=0, max_value=10, value=2, step=1)

    # Third search bar: Number of children levels to display
    children_limit = st.sidebar.number_input("Number of Children Levels", min_value=0, max_value=10, value=2, step=1)

    # Define a function to assign colors based on the level
    def get_color_by_level(level):
        colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ]
        return colors[level % len(colors)]

    # Define a function to assign specific colors to the nodes "Superclasses" and "Subclasses"
    def get_specific_node_color(node_name):
        if node_name == "Superclasses":
            return "#FFD700"  # Bright yellow for "Superclasses"
        elif node_name == "Subclasses":
            return "#1E90FF"  # Bright blue for "Subclasses"
        else:
            return None  # No specific color, use level-based color

    # Function to find parent nodes up to a certain level
    def find_parents(node_name, level, data, current_level=1):
        if level == 0:
            return []
        parents = []
        for item in data:
            if node_name in item["subclasses"].split(", "):
                color = get_specific_node_color(item["uniqueName"]) or get_color_by_level(current_level)
                parents.append({
                    "name": item["uniqueName"],
                    "children": find_parents(item["uniqueName"], level - 1, data, current_level + 1),
                    "color": color,
                    "description": item["description"]
                })
        return parents

    # Function to find child nodes up to a certain level
    def find_children(node_name, level, data, current_level=1):
        if level == 0:
            return []
        children = []
        for item in data:
            if node_name in item["superclasses"].split(", "):
                color = get_specific_node_color(item["uniqueName"]) or get_color_by_level(current_level)
                children.append({
                    "name": item["uniqueName"],
                    "children": find_children(item["uniqueName"], level - 1, data, current_level + 1),
                    "color": color,
                    "description": item["description"]
                })
        return children

    # Generate a filtered dataset based on the search term
    filtered_data = [item for item in data if item["uniqueName"] == search_term][0]

    # Prepare the hierarchical data for D3.js
    hierarchical_data = {
        "name": filtered_data["uniqueName"],
        "children": [
            {
                "name": "Superclasses",
                "children": find_parents(filtered_data["uniqueName"], parent_limit, data),
                "color": get_specific_node_color("Superclasses")  # Set specific color for "Superclasses"
            },
            {
                "name": "Subclasses",
                "children": find_children(filtered_data["uniqueName"], children_limit, data),
                "color": get_specific_node_color("Subclasses")  # Set specific color for "Subclasses"
            }
        ],
        "color": "red",  # The searched node remains red
        "description": filtered_data["description"]
    }

    # Convert hierarchical data to JSON format
    hierarchical_data_json = json.dumps(hierarchical_data)

    # Calculate the height and width dynamically based on the depth and number of nodes
    num_nodes = len(hierarchical_data['children'][0]['children']) + len(hierarchical_data['children'][1]['children']) + 1
    max_depth = max(parent_limit, children_limit)
    width = num_nodes * 650  # Increase spacing between nodes horizontally
    height = max_depth * 10  # Increase spacing between nodes vertically

    # Ensure a minimum size
    width = max(width, 1200)
    height = max(height, 1200)

    # Read the HTML template
    with open('d3_plot.html', 'r') as file:
        html_template = file.read()

    # Replace placeholders with data
    html_content = html_template.replace('{{data}}', hierarchical_data_json)
    html_content = html_content.replace('{{width}}', str(width))
    html_content = html_content.replace('{{height}}', str(height))

    # Display the D3.js graph
    st.components.v1.html(html_content, height=1000)

    st.header("D3.js Plot")

    # Display the D3.js graph with node descriptions on click, arrows on links, curved lines, a popup animation on hover, and panning/zooming
    components.html(html_content, height=1000)

    st.header("D3.js Plot")


