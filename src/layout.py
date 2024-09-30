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
