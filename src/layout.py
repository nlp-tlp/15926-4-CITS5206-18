import streamlit as st

def set_page_layout():
    """Set the Streamlit page layout to wide."""
    st.set_page_config(layout="wide")

def add_custom_css():
    """Add custom CSS for positioning the logo, footer, and setting the content width."""
    st.markdown(
        """
        <style>
        /* Sidebar width is set here */
        .sidebar {
            width: 300px;
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            z-index: 100;
            background-color: #f8f9fa;
            padding: 20px;
        }

        /* Main content width and height calculated based on sidebar width and dynamic height */
        .main-content {
            margin-left: 320px; /* Sidebar width + padding */
            padding: 20px;
            height: calc(100vh - 120px); /* View height minus header (50px) and footer (70px) */
            overflow: hidden; /* Disable scrolling */
            box-sizing: border-box; /* Ensure padding is included in height calculation */
        }

        /* Fix the header at the top */
        .header-container {
            position: fixed;
            top: 0; /* Make sure it sticks to the top */
            left: 320px; /* Sidebar width */
            width: calc(100% - 320px); /* Full width minus sidebar width */
            z-index: 100;
            background-color: #ffffff;
            padding: 5px 0; /* Adjust padding to reduce spacing */
            font-size: 6px; /* Make the font smaller */
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin: 0; /* Remove any margin to ensure it's at the top */
        }

        /* Fix the footer at the bottom */
        .content-footer {
            position: fixed;
            bottom: 0;
            left: 320px; /* Sidebar width */
            width: calc(100% - 320px); /* Full width minus sidebar */
            z-index: 100;
            background-color: #ffffff;
            padding: 1vh 0; /* Responsive padding using viewport height */
            text-align: center;
            font-size: 14px;
            /* Remove the border or shadow from the footer */
            box-shadow: none;
            height: auto; /* Allow the footer to adapt its height */
        }

        /* Ensure the model diagram height takes the remaining screen space */
        .model-diagram {
            position: relative;
            top: 50px; /* Adjust this value if your header height changes */
            height: 100vh;
            margin: 20px 0;
            overflow-y: auto; /* Enable scrolling if content exceeds the height */
        }

        /* Enhance button styling */
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            margin-top: 10px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #808080;
            color: white;
        }

        /* Style for mobile and desktop views */
        @media (max-width: 768px) {
            .content-footer {
                font-size: 12px;
                white-space: normal;
                word-wrap: break-word;
            }
        }

        @media (min-width: 769px) {
            .content-footer {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def end_main_content_wrapper():
    """Close the main content wrapper and add the footer within the content area."""
    st.markdown(
        '''
        <div class="content-footer">
            &copy;2024, Made For <b>"UWA NLP-TLP Group"</b>, Designed and Developed by <b>Manish Varada Reddy, Melo Xue, Shanmugapriya Sankarraj, Xudong Ying, Yu Xia, Zihan Zhang</b>.
        </div>
        ''',
        unsafe_allow_html=True
    )

def add_documentation_section():
    with st.expander("📚**DOCUMENTATION**📚"):
        st.markdown("""
        ## **Overview**
        The Interactive Visualization Tool for the ISO 15926-4 Standard helps users explore complex data relationships through two types of visualizations: a **Force-Directed Model** using NetworkX and a **Tree Model** using D3.js. These visualizations offer an interactive way to analyze and understand hierarchical relationships between entities.

        ## **Visualization Models**

        ### 1. **Force-Directed Model (Network Plot)**
        The Force-Directed Model presents a dynamic layout where nodes are attracted or repelled based on their relationships, creating an organic, real-time visualization of data connections.

        - **Dynamic Node Layout**: Nodes and edges rearrange themselves based on an algorithm that simulates physical forces, which helps visualize how entities are related in a flexible, interconnected manner.
        - **Color Legend**:
            - **Red**: Focus node (the node currently searched).
            - **Green**: Superclass nodes (parent entities).
            - **Blue**: Subclass nodes (child entities).

        ### 2. **Tree Model (Tree Plot)**
        The Tree Model organizes data hierarchically, where nodes are displayed in a structured tree format, with parent nodes connecting to child nodes.

        - **Static Hierarchical Layout**: This model arranges the nodes in a fixed, tree-like structure, making it easier to trace parent-child relationships and explore depth in the hierarchy.
        - **Color Legend**:
            - **Yellow**: Lines connecting superclass nodes (showing the parent-level relationships).
            - **Blue**: Lines connecting subclass nodes (showing child-level relationships).

        ## **Key Features**
        - **Search by Node Name**: Use the search bar to locate specific nodes by entering their name. The visualization will focus on the selected node.
        - **Filter by Levels**: Adjust the number of superclass or subclass levels displayed in the graph using the controls in the sidebar. This helps you focus on the immediate relationships or explore broader contexts.
        - **Search History**: Previous search results are stored in the sidebar. You can click on any previous search to restore the visualization state.
        - **Comparative Analysis**: Click the 'Enable Comparative' button to compare two nodes and their hierarchical relationships. Both nodes will be highlighted for easy comparison in the visualization.
        - **Navigation** Click on different model buttons to switch between the Force-Directed and Tree models for different perspectives on the data.
                    
        ## **Interaction Features**
        - **Click on a Node**: Displays the node's 'Definition' and 'Type' in the sidebar.
        - **Hover Over a Node**: Displays a floating tooltip showing the node's 'Definition' directly over it.
        - **Zoom and Pan**: Use your mouse or trackpad to zoom in/out and pan around the graph for detailed exploration.
        - **Fullscreen Mode**: Click the 'Fullscreen' button to enlarge the model for better visibility, and press 'Esc' to exit fullscreen.
        - **Export Graph**: Save the current graph as an image for reference or sharing with others.

        ## **Usage Guide**
        By following these steps, you can fully engage with the features of the Interactive Visualization Tool. From initial exploration to advanced comparison and export options, the tool is built to provide an intuitive and comprehensive way to navigate complex data relationships within the ISO 15926-4 dataset.

        ### Step 1: **Searching and Filtering Data**
        - **Find specific nodes and customize your view**:
            - **Search by Node Name**: Use the search bar to find specific nodes. Once you type the node's name, the visualization will focus on that node, making it easy to navigate directly to the entity you want to analyze.
            - **Filter by Levels**: Adjust the number of superclass and subclass levels displayed in the graph using the sidebar controls. This feature helps you focus on a small subset of relationships or explore a broader context by increasing the number of levels displayed.

        ### Step 2: **Switching Between Visualization Models**
        - **Toggle between the Force-Directed and Tree Models**:
            - Use the buttons under the navigation section to switch between the two models:
                - **Network Plot** (Force-Directed Model): A dynamic, interconnected visualization.
                - **Tree Plot** (D3.js Tree Model): A structured, hierarchical layout.
            - By default, the tool displays the **Tree Plot** when first loaded.

        ### Step 3: **Maximizing Visual Space**
        - **Enhance your view of the graph**:
            - **Fullscreen Mode**: For a better view, click the 'Fullscreen' button to expand the graph to fill your screen. This is especially helpful when dealing with large datasets or when presenting to others. To exit fullscreen, simply press 'Esc'.

        ### Step 4: **Exploring the Graph**
        - **Interact with nodes and explore their relationships**:
            - **Click on any Node**: When you click a node, its 'Definition' and 'Type' will be displayed in the sidebar. This helps you examine the specific characteristics of the node.
            - **Hover Over a Node**: Hovering over a node shows a floating tooltip with its 'Definition', giving you quick insights without needing to click.
            - **Zoom and Pan**: Use your mouse scroll or trackpad to zoom in and out of the graph. You can also click and drag to pan around the graph, helping you explore large datasets.

        ### Step 5: **Tracking and Revisiting Searches**
        - **Use the search history to revisit nodes**:
            - **Search History**: Every time you search for a node, the tool stores that result in the sidebar. You can click on any past search to instantly restore the graph to that state. This is useful for tracking your exploration and easily comparing previous findings.

        ### Step 6: **Comparing Multiple Nodes**
        - **Compare two nodes and their relationships**:
            - **Comparative Analysis**: Click the 'Enable Comparative' button to select two nodes for comparison. Both nodes will be highlighted in the graph, making it easy to visually compare their positions and hierarchical relationships.

        ### Step 7: **Exporting Your Graph**
        - **Save your findings**:
            - **Export Graph**: Once you’ve explored the graph and found key insights, you can export the current view as an image. This is useful for documentation, sharing with others, or including in reports or presentations.
                
        This tool is designed to make it easy to visualize and interact with ISO 15926-4 data, helping users explore complex relationships with dynamic, intuitive visualizations. Enjoy your journey into the hierarchical world of data!
        """)