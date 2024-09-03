import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
from networkx.readwrite import json_graph
import streamlit.components.v1 as components
import json

def display_networkx_plot(data, search_term, parent_limit, children_limit):
    """Display the NetworkX plot."""
    st.header("NetworkX Plot")

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

        # Reverse edges for superclasses (from the node to its superclass)
        for superclass in superclasses:
            if superclass:
                G.add_node(superclass)
                G.add_edge(unique_name, superclass)  # Reverse direction: node to superclass

        # Reverse edges for subclasses (from subclass to the node)
        for subclass in subclasses:
            if subclass:
                G.add_node(subclass)
                G.add_edge(subclass, unique_name)  # Reverse direction: subclass to node

    net = Network(height="1000px", width="100%", bgcolor="white", font_color="black", directed=True)

    if search_term and search_term in G:
        parent_nodes, child_nodes = apply_filtering(G, search_term, parent_limit, children_limit)
        sub_graph = G.subgraph(parent_nodes.union(child_nodes)).copy()
        net.from_nx(sub_graph)

        color_nodes(net, search_term, parent_nodes, child_nodes)
    else:
        net.from_nx(G)

    # Generate and display the PyVis graph in a temporary HTML file
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

    # Embed the generated HTML using Streamlit components
    components.html(f"""
        {graph_html}
        <script type="text/javascript">
            const graphData = {graph_json};

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
            }}

            // Tooltip for node hover
            const networkContainer = document.querySelector('.vis-network');
            const tooltip = document.createElement('div');
            tooltip.style.position = 'absolute';
            tooltip.style.padding = '5px 10px';
            tooltip.style.border = '1px solid #ccc';
            tooltip.style.backgroundColor = '#f9f9f9';
            tooltip.style.borderRadius = '5px';
            tooltip.style.display = 'none';
            tooltip.style.zIndex = '100';
            networkContainer.appendChild(tooltip);

            var network = window.network;

            network.on("click", function(params) {{
                if (params.nodes.length > 0) {{
                    var nodeId = params.nodes[0];
                    nodeClick(nodeId);
                }} else {{
                    const floatingBar = window.parent.document.getElementById('sidebarFloatingBar');
                    floatingBar.style.display = 'none';
                }}
            }});

            network.on("hoverNode", function(params) {{
                const nodeId = params.node;
                const node = graphData.nodes.find(n => n.id === nodeId);
                tooltip.innerHTML = node.title ? escapeHtml(node.title) : "No description available.";
                tooltip.style.display = 'block';
                tooltip.style.left = (params.event.center.x + 15) + 'px';
                tooltip.style.top = (params.event.center.y - 15) + 'px';
            }});

            network.on("blurNode", function(params) {{
                tooltip.style.display = 'none';
            }});
        </script>
    """, height=1000)

def apply_filtering(G, search_term, parent_limit, children_limit):
    """Apply filtering logic for displaying nodes."""
    parent_nodes = {search_term}
    current_level_nodes = {search_term}

    for _ in range(parent_limit):
        next_level_nodes = set()
        for node in current_level_nodes:
            next_level_nodes.update(G.predecessors(node))
        current_level_nodes = next_level_nodes - parent_nodes
        parent_nodes.update(current_level_nodes)

    child_nodes = {search_term}
    current_level_nodes = {search_term}

    for _ in range(children_limit):
        next_level_nodes = set()
        for node in current_level_nodes:
            next_level_nodes.update(G.successors(node))
        current_level_nodes = next_level_nodes - child_nodes
        child_nodes.update(current_level_nodes)

    return parent_nodes, child_nodes

def color_nodes(net, search_term, parent_nodes, child_nodes):
    """Color nodes in the NetworkX graph."""
    for node in net.nodes:
        node_id = node['id']  # Extract the node ID from the dictionary
        if node_id == search_term:
            net.get_node(node_id)["color"] = "red"
        elif node_id in parent_nodes:
            net.get_node(node_id)["color"] = "green"
        elif node_id in child_nodes:
            net.get_node(node_id)["color"] = "blue"
        else:
            net.get_node(node_id)["color"] = "white"