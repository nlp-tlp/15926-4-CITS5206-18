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
        <div class="footer" style="text-align: center; padding-left: 160px;">
            &copy;2024 , Made For <b>"UWA NLP-TLP Group"</b>, Designed and Developed by <b>Manish Varada Reddy, Melo Xue, Shanmugapriya Sankarraj, Xudong Ying, Yu Xia, Zihan Zhang<b>.
        </div>
        """,
        unsafe_allow_html=True
    )

def add_documentation_section():
    """Add the documentation section to the app."""
    with st.expander("📚**DOCUMENTATION**📚"):
        st.markdown("""
        ### How to Use the Interactive Graph Visualization Tool:
        
        **Overview:**
        This tool allows you to visualize hierarchical relationships using a directed graph. Nodes represent unique elements, and edges show parent-child relationships. The visualization utilizes D3.js and NetworkX to offer a dynamic, interactive experience.

        **Search Options:**
        - **Search by Unique Name:** Select a node to focus on by typing its name in the search bar.
        - **Number of Parent Levels:** Set the number of levels of parent nodes (ancestors) to display from the selected node.
        - **Number of Children Levels:** Set the number of levels of child nodes (descendants) to display from the selected node.

        **Graph Interaction Controls:**
        1. **NetworkX Plot:**
        - **Click on Nodes:** Clicking on a node will display its description in the sidebar.
        - **Hover Effects:** On hovering over a node, it shows a popup animation with the node's name and description.
        - **Node Colors:**
            - **Red:** The node you are focusing on.
            - **Green:** Parent nodes of the selected node.
            - **Blue:** Child nodes of the selected node.
        
        2. **D3.js Plot:**
        - **Click on Nodes:** Highlights the selected node and displays the node's description on the screen.
        - **Drag and Drop:** Nodes can be dragged around to better explore the graph layout.
        - **Zoom and Pan:** The D3.js graph supports zooming in/out and panning across the graph to dynamically explore different areas.
        - **Branch Colors:**
            - **Yellow:** Branches connecting all the PARENT nodes.
            - **Blue:** Branches connecting all the CHILDREN nodes, showing interconnected relationships around the selected node.

        **Controls:**
        - Adjust the levels using the side panel to dynamically update the displayed graph.
        - Use the search bars to refine the view based on node names and the number of parent/child nodes displayed.

        **Additional Features:**
        - **Auto-filling Search:** Search bars feature auto-fill suggestions to make finding nodes easier.
        - **Arrow Direction:** The direction of the arrows in the graph is set from the lowest node to the top, showing the hierarchy flow clearly.
                    
        ### How to Use the Interactive Graph Visualization Tool:
        1. **Start the Application:**
        - Launch the app by running the `streamlit run src/main.py` command in your terminal.
        2. **Input Your Search Criteria:**
        - Use the search bars on the side panel to specify your search preferences:
            - **Unique Name:** Type the name of the node you want to focus on.
            - **Number of Parent Levels:** Specify how many parent nodes (ancestors) to display for the selected node.
            - **Number of Children Levels:** Specify how many child nodes (descendants) to display for the selected node.
        3. **Interact with the Graph:**
        - Click on nodes to see their descriptions.
        - Use the side panel to adjust the view dynamically by changing the number of displayed parent and child nodes.
        - Hover, drag, and zoom to explore the graph interactively.

        Enjoy exploring your data with this interactive tool!
        """)
