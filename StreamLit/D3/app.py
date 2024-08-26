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

# Second search bar: Number of parent nodes to display
parent_limit = st.sidebar.number_input("Number of Parent Nodes", min_value=0, max_value=10, value=3, step=1)

# Third search bar: Number of children nodes to display
children_limit = st.sidebar.number_input("Number of Children Nodes", min_value=0, max_value=10, value=3, step=1)

# Generate a filtered dataset based on the search term
filtered_data = [item for item in data if item["uniqueName"] == search_term][0]

# Prepare the hierarchical data for D3.js
hierarchical_data = {
    "name": filtered_data["uniqueName"],
    "children": [
        {
            "name": "Superclasses",
            "children": [{"name": superclass, "color": "green", "description": filtered_data["description"]} for superclass in filtered_data["superclasses"].split(", ") if superclass]
        },
        {
            "name": "Subclasses",
            "children": [{"name": subclass, "color": "blue", "description": filtered_data["description"]} for subclass in filtered_data["subclasses"].split(", ") if subclass]
        }
    ],
    "color": "red",
    "description": filtered_data["description"]
}

# Convert hierarchical data to JSON format
hierarchical_data_json = json.dumps(hierarchical_data)

# Display the D3.js graph with node descriptions on click, arrows on links, curved lines, and a popup animation on hover
components.html(
    """
    <div id="d3-container" style="height: 1000px;"></div>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script>
        const data = """ + hierarchical_data_json + """;

        const width = 1000;
        const height = 800;

        const treeLayout = d3.tree().size([height, width]);

        const root = d3.hierarchy(data);

        treeLayout(root);

        const svg = d3.select("#d3-container").append("svg")
            .attr("width", width + 200)
            .attr("height", height + 200)
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
            .text(d => d.data.name);
    </script>
    """, 
    height=1000
)
