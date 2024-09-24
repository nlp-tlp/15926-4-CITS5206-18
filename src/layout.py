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

        /* Main content width calculated based on sidebar width */
        .main-content {
            margin-left: 320px; /* Sidebar width + padding */
            padding: 20px;
        }

        /* Fix the header at the top */
        .header-container {
            position: fixed;
            top: 0;
            left: 320px; /* Sidebar width */
            width: calc(100% - 320px); /* Full width minus sidebar width */
            z-index: 100;
            background-color: #ffffff;
            padding: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        /* Fix the footer at the bottom */
        .content-footer {
            position: fixed;
            bottom: 0;
            left: 320px; /* Sidebar width */
            width: calc(100% - 320px); /* Full width minus sidebar width */
            z-index: 100;
            background-color: #ffffff;
            padding: 10px 0;
            text-align: center;
            font-size: 14px;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
            line-height: 1.4;
        }

        /* Ensure the model diagram height takes the remaining screen space */
        .model-diagram {
            position: relative;
            top: 50px; /* Adjust this value if your header height changes */
            height: calc(100vh - 120px); /* 120px for header and footer combined */
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

def add_documentation_section():
    """Add the documentation section to the app."""
    with st.expander("📚**DOCUMENTATION**📚"):
        st.markdown("""
        ## **Overview**
        The Interactive Visualization Tool for the ISO 15926-4 Standard helps users explore hierarchical data relationships with D3.js and NetworkX visualizations. The tool is built with Streamlit, offering a user-friendly web interface. It visualizes nodes as unique elements and edges as superclass-subclass relationships. The interactive functionality allows users to explore data structures dynamically.

        ## **Search Options**
        - **Search by Unique Name**: Use the search bar to focus on a specific node.
        - **Number of Superclass Levels**: Adjust how many levels of superclass nodes to display.
        - **Number of Subclass Levels**: Adjust how many levels of subclass nodes to display.

        ## **Graph Interaction Controls**
        1. **Network Plot**:
            - **Click on Nodes**: Displays the node’s description and node types in the sidebar.
            - **Hover Effects**: Hovering on a node shows a tooltip with the node’s name and description.
            - **Node Colors**:
                - **Red**: Focus node.
                - **Green**: Superclass nodes.
                - **Blue**: Subclass nodes.

        2. **Tree Plot**:
            - **Click on Nodes**: Highlights the node, displays its description and node types.
            - **Drag and Drop**: Drag nodes to adjust their positions for better exploration.
            - **Zoom and Pan**: Supports zooming in/out and panning across the graph.
            - **Branch Colors**:
                - **Yellow**: Connects superclass nodes.
                - **Blue**: Connects subclass nodes.

        ## **How to Use the Tool**
        1. **Launch the Application**:
            - Run the app using the `streamlit run src/main.py` command.
            - The app opens in your default web browser.
            - Stop the app by pressing `Ctrl+C` in the terminal.
        2. **Input Search Criteria**:
            - **Unique Name**: Focus on a specific node by entering its name.
            - **Superclass/Subclass Levels**: Adjust the number of superclass/subclass nodes to display.
        3. **Explore the Graph**:
            - Click on nodes for descriptions.
            - Use the side panel to dynamically change the displayed number of superclass and subclass nodes.
            - Drag, zoom, and pan to explore the hierarchical relationships.
        4. **Search History**:
            - The search history is displayed in the sidebar.
            - Click on a history item to restore the previous search state.
        5. **Enable Comparative Analysis**:
            - Use the `Enable Comparative` button to enable the comparative analysis mode.
            - Select two nodes to compare their hierarchical relationships.
            - The nodes are highlighted in the graph for easy comparison.
        
        Enjoy exploring the hierarchical data with the interactive visualization tool!
        """)

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
