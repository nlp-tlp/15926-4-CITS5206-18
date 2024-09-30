import streamlit as st
import json
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile
from networkx.readwrite import json_graph

# Set the page layout to wide
st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        width: 100%;
    }
    .header-title {
        font-size: 3em;
        margin: 0;
        padding: 0;
    }
    .bottom-center {
        position: absolute;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1;
        font-size: 14px;
        color: #666666;
    }
    .stApp {
        background-color: #f0f0f0;
    }
    .stSidebar, .stHeader, .stText {
        font-size: 18px;
        color: #333333;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
    }
    .stSidebar .stButton button {
        background-color: #FF5733;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Create a header with title and logo
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<h1 class="header-title">Data Visualisation</h1>', unsafe_allow_html=True)
with col2:
    try:
        logo = Image.open('/Users/imac/Desktop/uwa.png')
        st.image(logo, width=150)
    except Exception as e:
        st.error(f"Error loading image: {e}")

# Toggle between two models
model_choice = st.sidebar.radio("Select Model", ["Model 1", "Model 2"])

# Sidebar for search options
st.sidebar.header("Search Options")

if model_choice == "Model 1":
    # Load JSON data
    with open('final_output.json') as json_file:
        data = json.load(json_file)
    
    # Extract unique names
    unique_names = [item["uniqueName"] for item in data]
    
    # Search options
    search_term = st.sidebar.selectbox("Search by Unique Name", unique_names)
    parent_limit = st.sidebar.number_input("Number of Parent Levels", min_value=0, max_value=10, value=2, step=1)
    children_limit = st.sidebar.number_input("Number of Children Levels", min_value=0, max_value=10, value=2, step=1)
    
    # Model 1 visualization code
    def get_color_by_level(level):
        colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ]
        return colors[level % len(colors)]

    def find_parents(node_name, level, data, current_level=1):
        if level == 0:
            return []
        parents = []
        for item in data:
            if node_name in item["subclasses"].split(", "):
                parents.append({
                    "name": item["uniqueName"],
                    "children": find_parents(item["uniqueName"], level - 1, data, current_level + 1),
                    "color": get_color_by_level(current_level),
                    "description": item["description"]
                })
        return parents

    def find_children(node_name, level, data, current_level=1):
        if level == 0:
            return []
        children = []
        for item in data:
            if node_name in item["superclasses"].split(", "):
                children.append({
                    "name": item["uniqueName"],
                    "children": find_children(item["uniqueName"], level - 1, data, current_level + 1),
                    "color": get_color_by_level(current_level),
                    "description": item["description"]
                })
        return children

    filtered_data = [item for item in data if item["uniqueName"] == search_term][0]

    hierarchical_data = {
        "name": filtered_data["uniqueName"],
        "children": [
            {
                "name": "Superclasses",
                "children": find_parents(filtered_data["uniqueName"], parent_limit, data)
            },
            {
                "name": "Subclasses",
                "children": find_children(filtered_data["uniqueName"], children_limit, data)
            }
        ],
        "color": "red",
        "description": filtered_data["description"]
    }

    hierarchical_data_json = json.dumps(hierarchical_data)

    num_nodes = len(hierarchical_data['children'][0]['children']) + len(hierarchical_data['children'][1]['children']) + 1
    max_depth = max(parent_limit, children_limit)
    width = max(num_nodes * 250, 1000)
    height = max(max_depth * 250, 800)

    components.html(
        f"""
        <div id="d3-container" style="height: 1000px;"></div>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
            const data = {hierarchical_data_json};

            const width = {width};
            const height = {height};

            const treeLayout = d3.tree().size([height, width]);

            const root = d3.hierarchy(data);

            treeLayout(root);

            const svg = d3.select("#d3-container").append("svg")
                .attr("width", width + 200)
                .attr("height", height + 200)
                .call(d3.zoom().on("zoom", function(event) {{
                    svg.attr("transform", event.transform);
                }}))
                .append("g")
                .attr("transform", "translate(100,100)");

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

            svg.selectAll('path.link')
                .data(root.links())
                .enter().append('path')
                .attr('class', 'link')
                .attr('d', d3.linkHorizontal()
                    .x(d => d.y)
                    .y(d => d.x)
                )
                .attr("fill", "none")
                .attr("stroke", "#ccc")
                .attr("stroke-width", 2)
                .attr("marker-end", "url(#arrow)");

            const tooltip = d3.select("#d3-container")
                .append("div")
                .style("position", "absolute")
                .style("visibility", "hidden")
                .style("background-color", "white")
                .style("border", "1px solid #ccc")
                .style("padding", "8px")
                .style("border-radius", "4px")
                .style("font-size", "12px");

            function escapeHtml(content) {{
                const div = document.createElement('div');
                div.textContent = content;
                return div.innerHTML;
            }}

            const node = svg.selectAll('circle')
                .data(root.descendants())
                .enter()
                .append('circle')
                .attr('cx', d => d.y)
                .attr('cy', d => d.x)
                .attr('r', 10)
                .style("fill", d => d.data.color || "#69b3a2")
                .on("mouseover", function(event, d) {{
                    tooltip.html(escapeHtml(d.data.description) || "No description available.")
                        .style("visibility", "visible")
                        .style("top", (event.pageY - 28) + "px")
                        .style("left", (event.pageX + 5) + "px");

                    d3.select(this).transition()
                        .duration(200)
                        .attr("r", 20);
                }})
                .on("mousemove", function(event, d) {{
                    tooltip.style("top", (event.pageY - 28) + "px")
                        .style("left", (event.pageX + 5) + "px");
                }})
                .on("mouseout", function(event, d) {{
                    tooltip.style("visibility", "hidden");

                    d3.select(this).transition()
                        .duration(200)
                        .attr("r", 10);
                }})
                .call(d3.drag()
                    .on("start", function(event, d) {{
                        d3.select(this).raise().attr("r", 20);
                    }})
                    .on("drag", function(event, d) {{
                        d3.select(this)
                            .attr("cx", d.x = event.x)
                            .attr("cy", d.y = event.y);
                    }})
                    .on("end", function(event, d) {{
                        d3.select(this).attr("r", 10);
                    }})
                );

            svg.selectAll('text')
                .data(root.descendants())
                .enter()
                .append('text')
                .attr('x', d => d.y + 15)
                .attr('y', d => d.x + 5)
                .attr('dy', -10)
                .attr('text-anchor', 'start')
                .style("font-size", "14px")
                .style("fill", "white")
                .style("overflow", "hidden")
                .style("text-overflow", "ellipsis")
                .style("max-width", "150px")
                .text(d => d.data.name.length > 20 ? d.data.name.slice(0, 20) + "..." : d.data.name);
        </script>
        """, 
        height=1000
    )

elif model_choice == "Model 2":
    # Load the new dataset
    data = pd.read_csv('Functional_Database_2-level.csv')
    
    # Search options
    unique_names = data['uniqueName'].tolist()
    search_term = st.sidebar.selectbox("Search by Unique Name", unique_names)
    parent_limit = st.sidebar.number_input("Number of Parent Nodes", min_value=0, max_value=10, value=3, step=1)
    children_limit = st.sidebar.number_input("Number of Children Nodes", min_value=0, max_value=10, value=3, step=1)
    
    # Model 2 visualization code
    G = nx.DiGraph()

    for index, row in data.iterrows():
        unique_name = row['uniqueName']
        
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

        description = str(row['description']) if not pd.isna(row['description']) else ""

        G.add_node(unique_name, title=description)
        
        for superclass in superclasses:
            if superclass:
                G.add_node(superclass)
                G.add_edge(unique_name, superclass)
        
        for subclass in subclasses:
            if subclass:
                G.add_node(subclass)
                G.add_edge(subclass, unique_name)

    net = Network(height="1000px", width="100%", bgcolor="#222222", font_color="white", directed=True)

    if search_term and search_term in G:
        parent_nodes = list(nx.ancestors(G, search_term))[:parent_limit]
        child_nodes = list(nx.descendants(G, search_term))[:children_limit]
        neighbors = list(G.neighbors(search_term))

        sub_graph = G.subgraph([search_term] + parent_nodes + child_nodes + neighbors).copy()

        pos = {}
        pos[search_term] = (0, 0)

        for i, parent in enumerate(parent_nodes):
            pos[parent] = (0, -(i + 1))

        for i, child in enumerate(child_nodes):
            pos[child] = (0, -(len(parent_nodes) + i + 1))

        net.from_nx(sub_graph)

        for node, (x, y) in pos.items():
            net.get_node(node)["x"] = x * 100
            net.get_node(node)["y"] = y * -100

            if node == search_term:
                net.get_node(node)["color"] = "red"
            elif node in parent_nodes:
                net.get_node(node)["color"] = "green"
            elif node in child_nodes:
                net.get_node(node)["color"] = "blue"
            else:
                net.get_node(node)["color"] = "white"

    else:
        net.from_nx(G)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        tmp_file.seek(0)
        graph_html = tmp_file.read().decode()

    graph_data = json_graph.node_link_data(G)
    graph_json = json.dumps(graph_data)

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

    components.html(f"""
    {graph_html}  <!-- Embed the PyVis graph -->
    <script type="text/javascript">
        // Parse the graph JSON data
        const graphData = {graph_json};

        // Function to escape HTML content
        function escapeHtml(content) {{
            const div = document.createElement('div');
            div.textContent = content;
            return div.innerHTML;
        }}

        // Function to handle node clicks
        function nodeClick(nodeId) {{
            //Find the node object in graphData using the nodeId
            const node = graphData.nodes.find(n => n.id === nodeId);
            
            // Display the node's title in the alert, fallback to nodeId if title is not available
            const nodeTitle = node && node.title ? node.title : nodeId;
            
            const floatingBar = window.parent.document.getElementById('sidebarFloatingBar');
            floatingBar.innerHTML =  escapeHtml(nodeTitle);
            floatingBar.style.display = 'block';

        }}

        // Ensure the network instance is properly accessed
        var network = window.network;  // Access the network directly
        network.on("click", function(params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                nodeClick(nodeId);
            }}
        }});
    </script>

""", height=1000)
    
# Add the copyright notice at the bottom center
st.markdown(
    """
    <div class="bottom-center">
        © 2024 UWA CITS5206 Group18. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)