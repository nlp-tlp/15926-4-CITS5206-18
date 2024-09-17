import streamlit as st
from layout import set_page_layout, add_custom_css, add_footer, add_documentation_section
from data_handler import load_data, extract_unique_names
from networkx_plot import display_networkx_plot
from d3js_plot import display_d3js_plot
import os

# Set the page layout to wide
set_page_layout()

# Add custom CSS for positioning the logo and footer
add_custom_css()

# Add the documentation section
add_documentation_section()

# Add the footer with copyright information
add_footer()

# Initialize session state for page selection
if 'page' not in st.session_state:
    st.session_state.page = "D3.js Plot"  # Default page

# Add the logo to the sidebar using st.image
st.sidebar.image("static/images/nlp-tlp-logo.png", width=130)

# Create a sidebar header
st.sidebar.header("Navigation")

# Revert to using Streamlit's native buttons
if st.sidebar.button("TREE Plot"):
    st.session_state.page = "D3.js Plot"

if st.sidebar.button("NETWORK Plot"):
    st.session_state.page = "NetworkX Plot"

# Construct absolute path to the JSON file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(base_dir, 'data', 'final_output.json')

# Load the dataset from JSON file
data = load_data(json_path)

# Create the sidebar for search bars
st.sidebar.header("Search Options")

# Extract unique names
unique_names = extract_unique_names(data)

# First search bar: Search by unique name with auto-fill
search_term = st.sidebar.selectbox("Search by Unique Name", unique_names)

# Input for the number of parent levels to display
parent_limit = st.sidebar.number_input("Number of Levels of Superclass", min_value=0, max_value=10, value=3, step=1)

# Input for the number of children levels to display
children_limit = st.sidebar.number_input("Number of Levels of Subclass", min_value=0, max_value=10, value=3, step=1)

# Header for Node description box
st.sidebar.header("Node Description")

# Sidebar for displaying node descriptions
with st.sidebar:
    st.markdown("""
        <div id="sidebarFloatingBar" style="
            background-color: #fff;
            color: black;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            display: none;">
        </div>
        """, unsafe_allow_html=True)

# Header for Node Types box
st.sidebar.header("Node Types")
    
# Sidebar for displaying node types
with st.sidebar:
    st.markdown("""
        <div id="nodeType" style="
            background-color: #fff;
            color: black;
            padding: 10px;
            border-radius: 5px;
            display: none;">
        </div>
        """, unsafe_allow_html=True)

# Display content based on the selected page
if st.session_state.page == "NetworkX Plot":
    display_networkx_plot(data, search_term, parent_limit, children_limit)
  
elif st.session_state.page == "D3.js Plot":
    display_d3js_plot(data, search_term, parent_limit, children_limit)