import streamlit as st

def set_page_layout():
    """Set the Streamlit page layout to wide."""
    st.set_page_config(layout="wide")

def add_custom_css():
    """Add custom CSS for positioning the logo and footer."""
    st.markdown(
        """
        <style>
        /* Position the logo at the bottom right */
        .logo-container {
            position: fixed;
            right: 10px;
            bottom: 10px;
            z-index: 100;
        }
        .logo-container img {
            width: 150px;  /* Adjust size as needed */
            opacity: 0.8;  /* Optional: adjust opacity */
        }

        /* Style for the footer */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: #000;
            text-align: center;
            padding: 10px 0;
            z-index: 99;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def add_footer():
    """Add footer with copyright information."""
    st.markdown(
        """
        <div class="footer">
            &copy;2024, Made For <b>"UWA NLP-TLP Group"</b>, Designed and Developed by <b>Manish Varada Reddy, Melo Xue, Shanmugapriya Sankarraj, Xudong Ying, Yu Xia, Zihan Zhang</b>.
        </div>
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
            - **Click on Nodes**: Displays the node’s description in the sidebar.
            - **Hover Effects**: Hovering on a node shows a tooltip with the node’s name and description.
            - **Node Colors**:
                - **Red**: Focus node.
                - **Green**: Superclass nodes.
                - **Blue**: Subclass nodes.

        2. **Tree Plot**:
            - **Click on Nodes**: Highlights the node and displays its description.
            - **Drag and Drop**: Drag nodes to adjust their positions for better exploration.
            - **Zoom and Pan**: Supports zooming in/out and panning across the graph.
            - **Branch Colors**:
                - **Yellow**: Connects superclass nodes.
                - **Blue**: Connects subclass nodes.

        ## **How to Use the Tool**
        1. **Launch the Application**:
            - Run the app using the `streamlit run src/main.py` command.
        2. **Input Search Criteria**:
            - **Unique Name**: Focus on a specific node by entering its name.
            - **Superclass/Subclass Levels**: Adjust the number of superclass/subclass nodes to display.
        3. **Explore the Graph**:
            - Click on nodes for descriptions.
            - Use the side panel to dynamically change the displayed number of superclass and subclass nodes.
            - Drag, zoom, and pan to explore the hierarchical relationships.
        
        Enjoy exploring the hierarchical data with the interactive visualization tool!
        """)