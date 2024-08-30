import streamlit as st
import json
import streamlit.components.v1 as components

# Set the page layout to wide
st.set_page_config(layout="wide")

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
width = num_nodes * 850  # Increase spacing between nodes horizontally
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
            .attr("stroke", "#ccc")
            .attr("stroke-width", 2)
            .attr("marker-end", "url(#arrow)");

        // Nodes with popup animation on hover and drag behavior
        const node = svg.selectAll('circle')
            .data(root.descendants())
            .enter()
            .append('circle')
            .attr('cx', d => d.y)
            .attr('cy', d => d.x)
            .attr('r', 10)
            .style("fill", d => d.data.color || "#69b3a2")
            .on("click", function(event, d) {{
                alert(d.data.description || "No description available.");
            }})
            .on("mouseover", function(event, d) {{
                d3.select(this).transition()
                    .duration(200)
                    .attr("r", 20);  // Increase radius on hover
            }})
            .on("mouseout", function(event, d) {{
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
            .style("overflow", "visible")  // Allow text to extend beyond its box
            .text(d => d.data.name);
    </script>
    """, 
    height=1000
)
