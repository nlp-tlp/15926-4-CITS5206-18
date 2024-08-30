import streamlit as st
import json
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import tempfile
from networkx.readwrite import json_graph

# Set the page layout to wide
st.set_page_config(layout="wide")

# Initialize session state for page selection
if 'page' not in st.session_state:
    st.session_state.page = "D3.js Plot"  # Default page

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

    # Load the new dataset from JSON file
    with open('final_output.json') as json_file:
        data = json.load(json_file)

    # Create the sidebar for search bars
    st.sidebar.header("Search Options")

    # Extract unique names
    unique_names = [item['uniqueName'] for item in data]

    # First search bar: Search by unique name with auto-fill
    search_term = st.sidebar.selectbox("Search by Unique Name", unique_names)

    # Second search bar: Number of parent nodes to display
    parent_limit = st.sidebar.number_input("Number of Parent Nodes", min_value=0, max_value=10, value=3, step=1)

    # Third search bar: Number of children nodes to display
    children_limit = st.sidebar.number_input("Number of Children Nodes", min_value=0, max_value=10, value=3, step=1)

    # Create a graph
    G = nx.DiGraph()

    # Add nodes and edges, including the description in the node's title (which is shown as a tooltip)
    for item in data:
        unique_name = item['uniqueName']
        
        # Handle potential NaN values in the superclasses and subclasses fields
        superclasses = item['superclasses'].split(', ') if 'superclasses' in item and item['superclasses'] else []
        subclasses = item['subclasses'].split(', ') if 'subclasses' in item and item['subclasses'] else []

        # Ensure description is always a string
        description = str(item['description']) if 'description' in item and item['description'] else ""

        # Add node to the graph with the description as a tooltip
        G.add_node(unique_name, title=description)  
        
        # Add edges for superclasses (reversing the direction)
        for superclass in superclasses:
            if superclass:
                G.add_node(superclass)
                G.add_edge(superclass, unique_name)  # Corrected edge direction for hierarchy
        
        # Add edges for subclasses (reversing the direction)
        for subclass in subclasses:
            if subclass:
                G.add_node(subclass)
                G.add_edge(unique_name, subclass)  # Corrected edge direction for hierarchy

    # Initialize the network graph visualization
    net = Network(height="1000px", width="100%", bgcolor="#222222", font_color="white", directed=True)

    # Filter the graph if a search term is provided
    if search_term and search_term in G:
        # Get parent nodes (ancestors) up to the specified limit
        parent_nodes = list(nx.ancestors(G, search_term))[:parent_limit]
        
        # Get child nodes (descendants) up to the specified limit
        child_nodes = list(nx.descendants(G, search_term))[:children_limit]

        # Include the search term and its direct neighbors
        sub_graph_nodes = [search_term] + parent_nodes + child_nodes
        sub_graph = G.subgraph(sub_graph_nodes).copy()

        # Generate network graph visualization
        net.from_nx(sub_graph)

        # Apply positions and set custom colors
        for node in sub_graph.nodes():
            # Set custom colors based on node type (search_term, parents, children)
            if node == search_term:
                net.get_node(node)["color"] = "red"  # Color for searched node
            elif node in parent_nodes:
                net.get_node(node)["color"] = "green"  # Color for parent nodes
            elif node in child_nodes:
                net.get_node(node)["color"] = "blue"  # Color for child nodes
            else:
                net.get_node(node)["color"] = "white"  # Default color for other nodes

    else:
        # If no search term is provided or the search term is not found, visualize the entire graph
        net.from_nx(G)

    # Adjust the height of the description box to accommodate the full text
    # Save the graph to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        tmp_file.seek(0)
        graph_html = tmp_file.read().decode()

    # Convert the graph to a JSON serializable format
    graph_data = json_graph.node_link_data(G)

    # Serialize the graph to JSON
    graph_json = json.dumps(graph_data)

    # Sidebar for displaying node descriptions
    with st.sidebar:
        # Add a div for the floating bar in the sidebar
        st.markdown("""
            <div id="sidebarFloatingBar" style="
                background-color: #fff;
                color: black;
                padding: 10px;
                border-radius: 5px;
                display: none;">
            </div>
            """, unsafe_allow_html=True)

    # JavaScript to handle node clicks using vis.js
    components.html("""
        """ + graph_html + """  <!-- Embed the PyVis graph -->
        <script type="text/javascript">
            // Parse the graph JSON data
            const graphData = """ + graph_json + """;

            // Function to escape HTML content
            function escapeHtml(content) {
                const div = document.createElement('div');
                div.textContent = content;
                return div.innerHTML;
            }

            // Function to handle node clicks
            function nodeClick(nodeId) {
                //Find the node object in graphData using the nodeId
                const node = graphData.nodes.find(n => n.id === nodeId);
                
                // Display the node's title in the alert, fallback to nodeId if title is not available
                const nodeTitle = node && node.title ? node.title : nodeId;
                
                const floatingBar = window.parent.document.getElementById('sidebarFloatingBar');
                floatingBar.innerHTML =  escapeHtml(nodeTitle);
                floatingBar.style.display = 'block';

            }

            // Ensure the network instance is properly accessed
            var network = window.network;  // Access the network directly
            network.on("click", function(params) {
                if (params.nodes.length > 0) {
                    var nodeId = params.nodes[0];
                    nodeClick(nodeId);
                }
            });
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

    # Display the D3.js graph with node descriptions on click, arrows on links, curved lines, a popup animation on hover, and panning/zooming
    components.html(
        """
        <div id="d3-container" style="height: 1000px;"></div>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
            const data = """ + hierarchical_data_json + """;

            const width = """ + str(width) + """;
            const height = """ + str(height) + """;

            const treeLayout = d3.tree().size([height, width]);

            const root = d3.hierarchy(data);

            treeLayout(root);

            const svg = d3.select("#d3-container").append("svg")
                .attr("width", width + 300)  // Add extra space to the right for labels
                .attr("height", height + 200)
                .call(d3.zoom().on("zoom", function(event) {
                    svg.attr("transform", event.transform);
                }))
                .append("g")
                .attr("transform", "translate(100,100)");

            // Define the arrowhead marker
            svg.append("defs").append("marker")
                .attr("id", "arrow")
                .attr("viewBox", "0 0 10 10")
                .attr("refX", 10)
                .attr("refY", 5)
                .attr("markerWidth", 6)
                .attr("markerHeight", 6)
                .attr("orient", "auto-start-reverse")
                .append("path")
                .attr("d", "M 0 0 L 10 5 L 0 10 z")
                .style("fill", "#ccc");

            // Links with arrows and curved lines
    svg.selectAll('path.link')
        .data(root.links())
        .enter().append('path')
        .attr('class', 'link')
        .attr('d', d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x)
        )
        .attr("fill", "none")
        .attr("stroke", function(d) {
            let source = d.source;
            while (source) {
                if (source.data.name.toUpperCase() === "SUPERCLASSES") {
                    return "#FFD700"; // Yellow color for "Superclasses"
                } else if (source.data.name.toUpperCase() === "SUBCLASSES") {
                    return "#1E90FF"; // Blue color for "Subclasses"
                }
                source = source.parent;
            }
            return "#ccc"; // Default color for other links
        })
        .attr("stroke-width", 2)
        .attr("marker-end", function(d) {
            let source = d.source;
            while (source) {
                if (source.data.name.toUpperCase() === "SUPERCLASSES") {
                    return "url(#arrow-superclasses)";
                } else if (source.data.name.toUpperCase() === "SUBCLASSES") {
                    return "url(#arrow-subclasses)";
                }
                source = source.parent;
            }
            return "url(#arrow)";
        });

    // Define the arrowhead markers with specific colors
    svg.append("defs").append("marker")
        .attr("id", "arrow-superclasses")
        .attr("viewBox", "0 0 10 10")
        .attr("refX", 10)
        .attr("refY", 5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto-start-reverse")
        .append("path")
        .attr("d", "M 0 0 L 10 5 L 0 10 z")
        .style("fill", "#FFD700"); // Yellow color for "Superclasses"

    svg.append("defs").append("marker")
        .attr("id", "arrow-subclasses")
        .attr("viewBox", "0 0 10 10")
        .attr("refX", 10)
        .attr("refY", 5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto-start-reverse")
        .append("path")
        .attr("d", "M 0 0 L 10 5 L 0 10 z")
        .style("fill", "#1E90FF"); // Blue color for "Subclasses"

    // Default arrow for other nodes
    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 0 10 10")
        .attr("refX", 10)
        .attr("refY", 5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto-start-reverse")
        .append("path")
        .attr("d", "M 0 0 L 10 5 L 0 10 z")
        .style("fill", "#ccc"); // Default color for other arrows



            // Nodes with popup animation on hover and drag behavior
            const node = svg.selectAll('circle')
            .data(root.descendants())
            .enter()
            .append('circle')
            .attr('cx', d => d.y)
            .attr('cy', d => d.x)
            .attr('r', d => {
                if (d.data.name === "Superclasses" || d.data.name === "Subclasses") {
                    return 20;  // Larger radius for "Superclasses" and "Subclasses"
                } else {
                    return 10;  // Default radius for other nodes
                }
            })
            .style("fill", d => d.data.color || "#69b3a2")
            .on("click", function(event, d) {
                alert(d.data.description || "No description available.");
            })
            .on("mouseover", function(event, d) {
                if (d.data.name !== "Superclasses" && d.data.name !== "Subclasses") {
                    d3.select(this).transition()
                        .duration(200)
                        .attr("r", 20);  // Increase radius on hover only for other nodes
                }
            })
            .on("mouseout", function(event, d) {
                if (d.data.name !== "Superclasses" && d.data.name !== "Subclasses") {
                    d3.select(this).transition()
                        .duration(200)
                        .attr("r", 10);  // Revert to original radius only for other nodes
                }
            });


            // Labels
            svg.selectAll('text')
                .data(root.descendants())
                .enter()
                .append('text')
                .attr('x', d => d.y + 15)
                .attr('y', d => d.x + 5)
                .attr('dy', -10)
                .attr('text-anchor', 'start')
                .style("font-size", "20px")
                .style("fill", "black")
                .style("font-weight", "bold")
                .style("overflow", "visible")  // Allow text to extend beyond its box
                .style("text-transform", d => (d.data.name === "Superclasses" || d.data.name === "Subclasses") ? "uppercase" : "none")
                .text(d => d.data.name);
        </script>
        """, 
        height=1000
    )

    st.header("D3.js Plot")
    

