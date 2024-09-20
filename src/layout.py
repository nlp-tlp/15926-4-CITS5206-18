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

       /* Fix the sidebar in place without locking its width */
        .css-1d391kg {  /* This targets the sidebar container */
            position: fixed !important;  /* Fix the sidebar in place */
            top: 0;
            left: 0;
            height: 100vh;  /* Sidebar takes the full height */
            z-index: 999;  /* Ensure it's above the content but below the footer */
            overflow-y: auto;  /* Allow scrolling if content overflows */
            width: 25%;  /* Set the sidebar width to 25% of the screen */
        }

        /* Ensure the main content doesn't overlap the sidebar */
        .css-18e3th9 {
            margin-left: 25% !important;  /* Reserve space for the sidebar */
            width: 75% !important;  /* Main content takes the remaining space */
        }

        /* Fix the footer at the bottom of the viewport */
        .content-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            color: #000;
            text-align: center;
            padding: 10px 0;
            background-color: #f0f0f0;
            z-index: 1000;  /* Ensure it's above the sidebar */
        }

        /* Prevent content overlap with the footer */
        .stApp {
            padding-bottom: 60px;  /* Leave space for the footer */
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

        /* Add a subtle box shadow to elements for depth */
        .stTextInput>div>div>input, .stSelectbox>div>div>select {
            box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
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
            - The app opens in your default web browser.
            - Stop the app by pressing `Ctrl+C` in the terminal.
        2. **Input Search Criteria**:
            - **Unique Name**: Focus on a specific node by entering its name.
            - **Superclass/Subclass Levels**: Adjust the number of superclass/subclass nodes to display.
        3. **Explore the Graph**:
            - Click on nodes for descriptions.
            - Use the side panel to dynamically change the displayed number of superclass and subclass nodes.
            - Drag, zoom, and pan to explore the hierarchical relationships.
        
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