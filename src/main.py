import streamlit as st
from layout import setup_layout, setup_footer, setup_sidebar
from data_handler import load_data
from networkx_plot import display_networkx_plot
from d3js_plot import display_d3js_plot

def main():
    """Main function to run the Streamlit app."""

    # Set the page layout to wide
    st.set_page_config(layout="wide")

    # Set up the layout and styling
    setup_layout()
    setup_footer()
    setup_sidebar()

    # Initialize session state for page selection
    if 'page' not in st.session_state:
        st.session_state.page = "D3.js Plot"  # Default page

    # Load the dataset
    data = load_data()

    # Extract unique names for the search options
    unique_names = [item['uniqueName'] for item in data]
    search_term = st.sidebar.selectbox("Search by Unique Name", unique_names)

    # Input for the number of parent and children levels to display
    parent_limit = st.sidebar.number_input("Number of Parent Levels", min_value=0, max_value=10, value=3, step=1)
    children_limit = st.sidebar.number_input("Number of Children Levels", min_value=0, max_value=10, value=3, step=1)

    # Display content based on the selected page
    if st.session_state.page == "NetworkX Plot":
        display_networkx_plot(data, search_term, parent_limit, children_limit)
    elif st.session_state.page == "D3.js Plot":
        display_d3js_plot(data, search_term, parent_limit, children_limit)

if __name__ == "__main__":
    main()