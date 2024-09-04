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
        <div class="footer" style="text-align: center; padding-left: 100px;">
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
        This tool allows you to visualize hierarchical relationships using a directed graph. Nodes represent unique elements, and edges show parent-child relationships.

        **Search Options:**
        - **Search by Unique Name:** Select a node to focus on.
        - **Number of Parent Levels:** Set the number of levels of parent nodes (ancestors) to display from the selected node.
        - **Number of Children Levels:** Set the number of levels of child nodes (descendants) to display from the selected node.

        **Graph Interaction:**
        - **Click on Nodes:** Clicking on a node will display its description in the sidebar.
        - **Node Colors:**
            - **Red:** The node you are focusing on.
            - **Green:** Parent nodes of the selected node.
            - **Blue:** Child nodes of the selected node.

        **Controls:**
        - Adjust the levels using the side panel to dynamically update the displayed graph.

        Enjoy exploring your data with this interactive tool!
                    
        TO RUN THE STREAMLIT CODE:

        **Install the related packages using:**

            pip install streamlit networkx pyvis pandas

        Run the Streamlit App:

        **Open a terminal or command prompt, navigate to the directory where your app.py file is located, and run the Streamlit app with the following command.**

            streamlit run app.py
        """)