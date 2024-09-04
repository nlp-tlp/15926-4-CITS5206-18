import streamlit as st

def setup_layout():
    """Set up custom CSS and layout for the app."""
    st.markdown(
        """
        <style>
        .logo-container {
            position: fixed;
            right: 10px;
            bottom: 10px;
            z-index: 100;
        }
        .logo-container img {
            width: 150px;
            opacity: 0.8;
        }
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
        .sidebar-logo img {
            width: 150px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def setup_footer():
    """Add footer to the app."""
    st.markdown(
        """
        <div class="footer" style="text-align: right; padding-right: 160px;">
            &copy;2024 , Made For <b>"UWA NLP-TLP Group"</b>, Designed and Developed by <b>Manish Varada Reddy, Melo Xue, Shanmugapriya Sankarraj, Xudong Ying, Yu Xia, Zihan Zhang</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

def setup_sidebar():
    """Set up the sidebar with logo and navigation."""
    st.sidebar.image("static/images/nlp-tlp-logo.png", width=130)
    st.sidebar.header("Navigation")

    if st.sidebar.button("D3.js Plot"):
        st.session_state.page = "D3.js Plot"

    if st.sidebar.button("NetworkX Plot"):
        st.session_state.page = "NetworkX Plot"