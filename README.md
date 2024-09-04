# Project Name: Interactive Visualization Tool for ISO 15926-4 Standard

This project is an interactive visualization tool for the ISO 15926-4 standard, designed to help users explore complex data relationships using NetworkX and D3.js visualizations. The application is built using Streamlit, providing an intuitive and interactive web interface.

## Table of Contents
- [Project Name: Interactive Visualization Tool for ISO 15926-4 Standard](#project-name-interactive-visualization-tool-for-iso-15926-4-standard)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [Modules](#modules)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

To run this project locally, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/nlp-tlp/15926-4-CITS5206-18.git
    cd 15926-4-CITS5206-18
    ```

2. **Create a Virtual Environment:**

    It is recommended to use a virtual environment to manage dependencies. Run the following commands to create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Dependencies:**

    Install all the required dependencies automatically using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit Application:**

    ```bash
    streamlit run src/main.py
    ```

## Project Structure
```
The project has been structured into multiple modules for better organization and maintainability:
14926-4-CITS5206-18
│
├── src/
│   ├── init.py                 # Initialize src package
│   ├── main.py                     # Main application entry point
│   ├── layout.py                   # Functions related to layout and styling
│   ├── data_handler.py             # Data loading functions
│   ├── networkx_plot.py            # NetworkX plot visualization functions
│   ├── d3js_plot.py                # D3.js plot visualization functions
│   └── utils.py                    # Utility functions
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── d3_plot.html                # D3.js plot HTML template
│
├── data/
│   └── final_output.json           # Data source file
│
├── script/
│   └── data_retrieve.py            # Update Dataset
│
├── docs/
│   └── 
|
├── requirements.txt                # List of dependencies
└── README.md
```
## Usage

To use the interactive visualization tool:

1. **Run the application** using the Streamlit command provided above.
2. **Navigate between visualizations**:
   - **NetworkX Plot**: Visualize complex relationships using NetworkX. Click on nodes to display definitions in the sidebar. Hover over nodes to see tooltips with additional information.
   - **D3.js Plot**: Explore hierarchical data relationships using a D3.js tree visualization.

3. **Search and Filter Options**:
   - Use the sidebar to search for specific nodes and adjust the number of parent and child levels displayed in the visualization.

## Modules

- **`main.py`**: The entry point of the application that initializes the Streamlit app and coordinates between different modules.
- **`layout.py`**: Contains functions to set up the layout and styling of the Streamlit interface.
- **`data_handler.py`**: Handles loading and processing of data from JSON files.
- **`networkx_plot.py`**: Contains the logic for rendering the NetworkX plot and handling user interactions.
- **`d3js_plot.py`**: Manages the D3.js plot rendering and data preparation.
- **`utils.py`**: Provides utility functions used across the application.

## Contributing

We welcome contributions to enhance the functionality and usability of this tool. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to reach out with any questions or suggestions for improvement!
