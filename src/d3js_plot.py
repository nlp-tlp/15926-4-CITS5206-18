import streamlit as st
import json
import streamlit.components.v1 as components

def display_d3js_plot(data, search_term, parent_limit, children_limit):
    """Display the D3.js plot with user-defined parameters."""

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
    
    # Create mappings for quick access
    uniqueName_to_node = { item['uniqueName']: item for item in data }
    
    # -------------------------------------------
    # Recursive Function to Find Parent Nodes
    # -------------------------------------------
    def find_parents(node_name, level, data, current_level=1, visited=None):
        # Initialize the visited set if it's the first call
        if visited is None:
            visited = set()

        # Base case: stop recursion if no more levels to traverse or node already
        if level == 0 or node_name in visited:
            return []
        
        # Mark the current node as visited to prevent revisiting
        visited.add(node_name)
        parents = []
        # Retrieve the current node's data using the mapping
        node = uniqueName_to_node.get(node_name)
        if not node:
            # If the node is not found in the mapping, return an empty list
            return []
        
        # Get the list of superclasses (parent nodes) for the current node
        superclasses = node.get('superclasses', '')
        # Split the superclasses string into a list, stripping any extra whitespace
        superclasses_list = [s.strip() for s in superclasses.split(',') if s.strip()]
        # Iterate over each superclass to build the parent hierarchy
        for parent_name in superclasses_list:
            if parent_name in uniqueName_to_node:
                # Determine the color for the parent node
                color = get_specific_node_color(parent_name) or get_color_by_level(current_level)
                # Retrieve the parent node's data
                parent_node = uniqueName_to_node[parent_name]
                 # Recursively find the parent's parents
                parents.append({
                    "name": parent_name,
                    "children": find_parents(parent_name, level - 1, data, current_level + 1, visited),
                    "color": color,
                    "description": parent_node.get("description", "No description available."),
                    "types": parent_node.get("types", "Unknown")
                })
        return parents

    # -------------------------------------------
    # Recursive Function to Find Childe Nodes
    # -------------------------------------------
    def find_children(node_name, level, data, current_level=1, visited=None):
        # Initialize the visited set if it's the first call
        if visited is None:
            visited = set()

        # Base case: stop recursion if no more levels to traverse or node already
        if level == 0 or node_name in visited:
            return []
        # Mark the current node as visited to prevent revisiting
        visited.add(node_name)
        children = []
        node = uniqueName_to_node.get(node_name)
        if not node:
            # If the node is not found in the mapping, return an empty list
            return []
        
        # Retrieve the 'subclasses' field and split it into a list
        subclasses = node.get('subclasses', '')
        subclasses_list = [s.strip() for s in subclasses.split(',') if s.strip()]
        for child_name in subclasses_list:
            if child_name in uniqueName_to_node:
                # Determine the color for the child node
                color = get_specific_node_color(child_name) or get_color_by_level(current_level)
                child_node = uniqueName_to_node[child_name]
                # Recursively find the children of the current child node
                children.append({
                    "name": child_name,
                    "children": find_children(child_name, level - 1, data, current_level + 1, visited),
                    "color": color,
                    "description": child_node.get("description", "No description available."),
                    "types": child_node.get("types", "Unknown")
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
                "children": find_parents(filtered_data["uniqueName"], parent_limit,data),
                "color": get_specific_node_color("Superclasses")  # Set specific color for "Superclasses"
            },
            {
                "name": "Subclasses",
                "children": find_children(filtered_data["uniqueName"], children_limit,data),
                "color": get_specific_node_color("Subclasses")  # Set specific color for "Subclasses"
            }
        ],
        "color": "red",  # The searched node remains red
        "description": filtered_data.get("description", "No description available."),
        "types": filtered_data.get("types", "Unknown")
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
    <!-- D3 Container -->
<div id="d3-container" style="height: 700px; padding: 0; margin: 10px; 
    border: 5px solid transparent;  /* Create space for the border */
    border-image: linear-gradient(90deg, #FFD700, #002855) 1;  /* Gradient matching NLP TLP logo */
    box-sizing: border-box; /* Ensure padding and border are included in width and height calculations */
    box-shadow: 0 0 10px rgba(0,0,0,0.05); overflow: hidden;">
</div>

<!-- Fullscreen Button below the D3 container -->
<div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
    <button id="fullscreen-btn" onclick="toggleFullscreen()" style="
        padding: 15px 20px; 
        font-size: 16px; 
        background: linear-gradient(90deg, #FFD700, #002855);  /* Gradient from light blue to yellow */
        color: white;  /* Text color */
        border: 3px solid #002855;  /* Navy blue border */
        border-radius: 5px; 
        cursor: pointer; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        Go Fullscreen For TREE PLOT
    </button>
</div>



            <script>
                function toggleFullscreen() {
                    const elem = document.getElementById('d3-container');
                    if (!document.fullscreenElement) {
                        elem.style.backgroundColor = "white";  // Set background color to white in fullscreen
                        elem.style.width = "100vw";  // Fullscreen width
                        elem.style.height = "100vh";  // Fullscreen height
                        elem.requestFullscreen().catch(err => {
                            alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
                        });
                    } else {
                        elem.style.width = "";  // Reset to default width
                        elem.style.height = "";  // Reset to default height
                        document.exitFullscreen();
                    }
                }

                // Automatically reset when exiting fullscreen
                document.addEventListener('fullscreenchange', function () {
                    const elem = document.getElementById('d3-container');
                    const buttonContainer = document.getElementById('button-container');

                    if (!document.fullscreenElement) {
                        elem.style.width = "100%";  // Reset to default width
                        elem.style.height = "700px";  // Reset to default height
                        buttonContainer.style.display = "flex";  // Show the button after exiting fullscreen
                    }
                });
            </script>



        <div id="tooltip" style="position: absolute; display: none; background: #fff; border: 1px solid #ccc; padding: 10px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1);"></div>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
            const data = """ + hierarchical_data_json + """;

            const width = """ + str(width) + """;
            const height = """ + str(height) + """;

            // Set the fixed node size (width and height) and spacing between nodes
            const treeLayout = d3.tree().nodeSize([50, 400]);

            const root = d3.hierarchy(data);

            treeLayout(root);

            const svg = d3.select("#d3-container").append("svg")
                .attr("width", "100%")  // Set svg width to 100% of the container
                .attr("height", "100%")  // Set svg height to 100% of the container
                .call(d3.zoom().on("zoom", function(event) {
                    svg.attr("transform", event.transform);
                }))
                .append("g")
                .attr("transform", "translate(100,100)");

            // Offset function to avoid label overlap
            function avoidLabelOverlap(node, i, nodes) {
                let x = node.y;
                let y = node.x;

                // Iterate over previous nodes
                for (let j = 0; j < i; j++) {
                    let prevNode = nodes[j];

                    // Check if the previous node is too close to the current node
                    if (Math.abs(prevNode.x - y) < 20 && Math.abs(prevNode.y - x) < 100) {
                        // Adjust the y position to avoid overlap
                        y = prevNode.x + 30;  // 30 is a pixel offset
                    }
                }
                return { x: x, y: y };
            }

            // Apply the offset to text labels
            svg.selectAll('text')
                .data(root.descendants())
                .enter()
                .append('text')
                .attr('x', (d, i) => avoidLabelOverlap(d, i, root.descendants()).x + 15)
                .attr('y', (d, i) => avoidLabelOverlap(d, i, root.descendants()).y + 5)
                .attr('dy', -10)
                .attr('text-anchor', 'start')
                .style("font-size", "20px")
                .style("fill", "black")
                .style("font-weight", "bold")
                .style("overflow", "visible")  // Allow text to extend beyond its box
                .style("text-transform", d => (d.data.name === "Superclasses" || d.data.name === "Subclasses") ? "uppercase" : "none")
                .text(d => truncateNodeName(d.data.name))
                .append("title")
                .text(d => d.data.name);

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

            // Function to escape HTML content
            function escapeHtml(content) {{
                const div = document.createElement('div');
                div.textContent = content;
                return div.innerHTML;
            }}

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
                    const floatingBar = window.parent.document.getElementById('sidebarFloatingBar');
                    floatingBar.innerHTML = d.data.description ? escapeHtml(d.data.description) : "No description available.";
                    floatingBar.style.display = 'block';

                    //To display node types information
                    const nodeType = window.parent.document.getElementById('nodeType');
                    nodeType.innerHTML = d.data.types ? escapeHtml(d.data.types) : "No Information available.";
                    nodeType.style.display = 'block';
                })
        
                .on("mouseover", function(event, d) {
                    if (d.data.name !== "Superclasses" && d.data.name !== "Subclasses") {
                        d3.select(this).transition()
                            .duration(200)
                            .attr("r", 20);  // Increase radius on hover only for other nodes
                    }
                    const tooltip = d3.select("#tooltip");
                    tooltip.style("display", "block")
                        .html(d.data.description ? escapeHtml(d.data.description) : "No description available.")
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY + 10) + "px");
                })
                .on("mouseout", function(event, d) {
                    if (d.data.name !== "Superclasses" && d.data.name !== "Subclasses") {
                        d3.select(this).transition()
                            .duration(200)
                            .attr("r", 10);  // Revert to original radius only for other nodes
                    }
                    const tooltip = d3.select("#tooltip");
                    tooltip.style("display", "none");  // Hide the tooltip when the mouse moves away
                });

            // Function to truncate node names if they are too long and append "..."
            function truncateNodeName(name, maxLength = 25) {
                if (name.length > maxLength) {
                    return name.substring(0, maxLength - 15) + "...";
                }
                return name;
            }

            // Update labels to display truncated names and show full name on hover
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
                .text(d => truncateNodeName(d.data.name))  // Truncate the name if it's too long
                .append("title")  // Tooltip with the full name on hover
                .text(d => d.data.name);  // Show full name on hover

        </script>
        """, 
        height=800
    )
