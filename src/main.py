import streamlit as st
from layout import set_page_layout, add_custom_css, end_main_content_wrapper
from data_handler import load_data, extract_unique_names
from networkx_plot import display_networkx_plot
from d3js_plot import display_d3js_plot
import os
from typing import List

 # Search history functions
def initialize_search_history() -> None:
    """Initialize the search history in the session state if it doesn't exist."""
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []

def add_to_search_history(term: str, max_history: int = 5) -> None:
    """
    Add a search term to the history, maintaining the maximum number of entries.
    
    Args:
    term (str): The search term to add to the history.
    max_history (int): The maximum number of search terms to keep in history.
    """
    if term not in st.session_state.search_history:
        st.session_state.search_history.append(term)
        # Keep only the last 'max_history' searches
        st.session_state.search_history = st.session_state.search_history[-max_history:]

def display_search_history() -> None:
    """Display the search history in the sidebar."""
    st.sidebar.write("Recent Searches:")
    for term in reversed(st.session_state.search_history):
        if st.sidebar.button(f"🔍 {term}", key=f"history_{term}"):
            # If a history item is clicked, update the search term
            st.session_state.search_term = term

# Set the page layout to wide
set_page_layout()

# Add custom CSS for positioning the logo and footer
add_custom_css()

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

# Initialize search history
initialize_search_history()

# Initialize search term in session state if it doesn't exist
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""

# First search bar: Search by unique name with auto-fill
search_term = st.sidebar.selectbox(
    "Search by Unique Name", 
    unique_names,
    index=unique_names.index(st.session_state.search_term) if st.session_state.search_term in unique_names else 0,
    help="Enter or select a node name to focus on in the visualization."
)

# Update search history when a new search is performed
if search_term != st.session_state.search_term:
    add_to_search_history(search_term)
    st.session_state.search_term = search_term

# Input for the number of parent levels to display
parent_limit = st.sidebar.number_input(
    "Number of Levels of Superclass", 
    min_value=0, 
    max_value=10, 
    value=3, 
    step=1,
    help="Specify how many levels of superclasses to display above the selected node."
)

# Input for the number of children levels to display
children_limit = st.sidebar.number_input(
    "Number of Levels of Subclass", 
    min_value=0, 
    max_value=10, 
    value=3, 
    step=1,
    help="Specify how many levels of subclasses to display below the selected node."
)

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

# Display search history after Node Types
st.sidebar.header("Search History")
display_search_history()
    
# Add a checkbox to enable comparative view
enable_comparative = st.sidebar.checkbox("Enable Comparative View")

if enable_comparative:
    # Create two columns for selecting nodes to compare
    col1, col2 = st.columns(2)
    
    with col1:
        # Dropdown to select the first node
        search_term1 = st.selectbox(
            "Select First Node",
            unique_names,
            key="search1",
            help="Select the first node for comparison"
        )
    
    with col2:
        # Dropdown to select the second node
        search_term2 = st.selectbox(
            "Select Second Node",
            unique_names,
            key="search2",
            help="Select the second node for comparison"
        )

    # Create two columns for selecting plot types to compare
    col1, col2 = st.columns(2)
    
    with col1:
        # Dropdown to select the plot type for the first node
        chart_type1 = st.selectbox(
            "Select First Plot Type",
            ["D3.js Plot", "NetworkX Plot"],
            key="chart_type1",
            help="Select the plot type for the first node"
        )
    
    with col2:
        # Dropdown to select the plot type for the second node
        chart_type2 = st.selectbox(
            "Select Second Plot Type",
            ["D3.js Plot", "NetworkX Plot"],
            key="chart_type2",
            help="Select the plot type for the second node"
        )

    # Create two columns for displaying comparative plots
    col1, col2 = st.columns(2)
    
    with col1:
        # Display plot for the first selected node based on the selected plot type
        if chart_type1 == "D3.js Plot":
            display_d3js_plot(data, search_term1, parent_limit, children_limit)
        else:
            display_networkx_plot(data, search_term1, parent_limit, children_limit)
    
    with col2:
        # Display plot for the second selected node based on the selected plot type
        if chart_type2 == "D3.js Plot":
            display_d3js_plot(data, search_term2, parent_limit, children_limit)
        else:
            display_networkx_plot(data, search_term2, parent_limit, children_limit)

else:
    # If comparative view is not enabled, display a single plot
    if st.session_state.page == "NetworkX Plot":
        display_networkx_plot(data, search_term, parent_limit, children_limit)
    elif st.session_state.page == "D3.js Plot":
        display_d3js_plot(data, search_term, parent_limit, children_limit)

# Add footer
end_main_content_wrapper()