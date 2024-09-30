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
        The Interactive Visualization Tool for the ISO 15926-4 Standard helps users explore complex data relationships using both NetworkX and D3.js visualizations. The tool is built with Streamlit, offering an intuitive web interface to visualize nodes and edges representing superclass-subclass relationships. The interactive functionality allows users to dynamically explore the data structures.

        ## **Search Options**
        - **Search by Unique Name**: Use the search bar to locate a specific node by its unique name.
        - **Number of Superclass Levels**: Adjust how many levels of superclass nodes to display.
        - **Number of Subclass Levels**: Adjust how many levels of subclass nodes to display.

        ## **Graph Interaction Controls**
        ### 1. **NetworkX Plot**:
            - **Click on Nodes**: Displays the node's 'Definition' and 'Type' in the sidebar.
            - **Hover Effects**: Hovering over a node shows a floating window with the node's 'Definition'.
            - **Node Colors**:
                - **Red**: Focus node.
                - **Green**: Superclass nodes.
                - **Blue**: Subclass nodes.
        
        ### 2. **D3.js Tree Plot**:
            - **Click on Nodes**: Highlights the node and displays its 'Definition' and 'Type'.
            - **Hover Effects**: Hovering over a node shows a floating tooltip with the node's 'Definition'.
            - **Drag and Drop**: Drag nodes to adjust their positions for better exploration.
            - **Zoom and Pan**: Supports zooming in/out and panning across the graph for better viewing.
            - **Branch Colors**:
                - **Yellow**: Connects superclass nodes.
                - **Blue**: Connects subclass nodes.
        
        ### 3. **Fullscreen Mode**:
            - **Fullscreen Button**: Click the 'Fullscreen' button to enable fullscreen mode for the graph.
            - **Exit Fullscreen**: Press 'Esc' to exit fullscreen mode.

        ## **How to Use the Tool**
        1. **Input Search Criteria**:
            - **Unique Name**: Focus on a specific node by entering its unique name.
            - **Superclass/Subclass Levels**: Adjust the number of superclass/subclass nodes to display.
        2. **Explore the Graph**:
            - Click on nodes to display their 'Definition' and 'Type' in the sidebar.
            - Hover over nodes to see a floating window displaying their 'Definition'.
            - Use the side panel to dynamically change the number of displayed superclass and subclass nodes.
            - Drag, zoom, and pan to explore relationships.
            - Enter fullscreen mode for an immersive experience, and press 'Esc' to exit fullscreen.

        Enjoy exploring the hierarchical data with the interactive visualization tool!
        """)