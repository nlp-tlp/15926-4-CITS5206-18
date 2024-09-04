import streamlit as st
import json
import streamlit.components.v1 as components
from PIL import Image

# Set the page layout to wide
st.set_page_config(layout="wide")

###################
# Custom CSS for background, text size, and tag color
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
        background-color: #f0f0f0;  /* Change background color */
    }
    .stSidebar, .stHeader, .stText {
        font-size: 18px;  /* Change text size */
        color: #333333;  /* Change text color */
    }
    .stButton button {
        background-color: #4CAF50;  /* Change button background color */
        color: white;  /* Change button text color */
        border-radius: 12px;
    }
    .stSidebar .stButton button {
        background-color: #FF5733;  /* Change button background color in sidebar */
        color: white;  /* Change button text color */
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
#####################

# Toggle between two models
model_choice = st.sidebar.radio("Select Model", ["Model 1", "Model 2"])
###################

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

# Function to find parent nodes up to a certain level
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

# Function to find child nodes up to a certain level
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

# Generate a filtered dataset based on the search term
filtered_data = [item for item in data if item["uniqueName"] == search_term][0]

# Prepare the hierarchical data for D3.js
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
    "color": "red",  # The searched node remains red
    "description": filtered_data["description"]
}

# Convert hierarchical data to JSON format
hierarchical_data_json = json.dumps(hierarchical_data)

# Calculate the height and width dynamically based on the depth and number of nodes
num_nodes = len(hierarchical_data['children'][0]['children']) + len(hierarchical_data['children'][1]['children']) + 1
max_depth = max(parent_limit, children_limit)
width = num_nodes * 250  # Increase spacing between nodes horizontally
height = max_depth * 250  # Increase spacing between nodes vertically

# Ensure a minimum size
width = max(width, 1000)
height = max(height, 800)

# Display the D3.js graph with node descriptions on hover
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
            .attr("width", width + 200)
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
            .attr("stroke", "#ccc")
            .attr("stroke-width", 2)
            .attr("marker-end", "url(#arrow)");

        // Tooltip for node descriptions
        const tooltip = d3.select("#d3-container")
            .append("div")
            .style("position", "absolute")
            .style("visibility", "hidden")
            .style("background-color", "white")
            .style("border", "1px solid #ccc")
            .style("padding", "8px")
            .style("border-radius", "4px")
            .style("font-size", "12px");

        // Function to escape HTML content
        function escapeHtml(content) {
            const div = document.createElement('div');
            div.textContent = content;
            return div.innerHTML;
        }

        // Nodes with popup animation on hover and drag behavior
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
                    .attr("r", 20);  // Increase radius on hover
            }})
            .on("mousemove", function(event, d) {{
                tooltip.style("top", (event.pageY - 28) + "px")
                    .style("left", (event.pageX + 5) + "px");
            }})
            .on("mouseout", function(event, d) {{
                tooltip.style("visibility", "hidden");

                d3.select(this).transition()
                    .duration(200)
                    .attr("r", 10);  // Revert to original radius
            }})
            .call(d3.drag()  // Add drag behavior
                .on("start", function(event, d) {{
                    d3.select(this).raise().attr("r", 20);  // Highlight node on drag start
                }})
                .on("drag", function(event, d) {{
                    d3.select(this)
                        .attr("cx", d.x = event.x)
                        .attr("cy", d.y = event.y);
                }})
                .on("end", function(event, d) {{
                    d3.select(this).attr("r", 10);  // Revert to original size on drag end
                }})
            );

        // Labels
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
            .style("max-width", "150px")  // Limit the width of text
            .text(d => d.data.name.length > 20 ? d.data.name.slice(0, 20) + "..." : d.data.name);
    </script>
    """, 
    height=1000
)

###################
# Add the copyright notice at the bottom center
st.markdown(
    """
    <div class="bottom-center">
        © 2024 UWA CITS5206 Group18. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
###################