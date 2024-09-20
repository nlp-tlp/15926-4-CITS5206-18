# Project Name: Interactive Visualization Tool for ISO 15926-4 Standard

This project is an interactive visualization tool for the ISO 15926-4 standard, designed to help users explore complex data relationships using NetworkX and D3.js visualizations. The application is built using Streamlit, providing an intuitive and interactive web interface.

## Table of Contents

- [Project Name: Interactive Visualization Tool for ISO 15926-4 Standard](#project-name-interactive-visualization-tool-for-iso-15926-4-standard)
  - [Table of Contents](#table-of-contents)
  - [Data Retrieval](#data-retrieval)
  - [Installation](#installation)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [Modules](#modules)
  - [Contributing](#contributing)
  - [Copyright](#copyright)

## Data Retrieval

To retrieve the latest DATA from the ENDPOINT:

```bash
python3 scripts/data_retrieve.py
```

## Installation

To run this project locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/nlp-tlp/15926-4-CITS5206-18.git
   cd 15926-4-CITS5206-18
   ```

2. **Install Required Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Application:**

   ```bash
   streamlit run src/main.py
   ```
4. **Stop the Streamlit Application:**

   ```bash
   Control + C
   ```

## Project Structure

```
src/
├── main.py                     # Main application entry point
├── layout.py                   # Functions related to layout and styling
├── data_handler.py             # Data loading functions
├── networkx_plot.py            # NetworkX plot visualization functions
├── d3js_plot.py                # D3.js plot visualization functions
└── templates
    ├── d3js_template.html      # Tree template
    └── networkx_template.html  # Network template
static/
└── images/
    └── nlp-tlp-logo.png
data/
├── filtered_out_data.jason     # Data including invalid nodes
└── final_output.json           # Data source file
requirements.txt                # List of dependencies
README.md
```

## Usage

To use the interactive visualization tool:

1. **Run the application** using the Streamlit command provided above.
2. **Navigate between visualizations**:
   - **NetworkX Plot**: Visualize relationships using NetworkX. Click on nodes to display definitions in the sidebar. Hover over nodes to see tooltips.
   - **D3.js Plot**: Explore hierarchical data relationships using a D3.js tree visualization.
3. **Search and Filter Options**:
   - Use the sidebar to search for specific nodes and adjust the number of parent and child levels displayed in the visualization.
4. **Search History**:
   - The search history is displayed in the sidebar.
   - Click on a history item to restore the previous search state.
5. **Enable Comparative Analysis**:
   - Use the `Enable Comparative` button to enable the comparative analysis mode.
   - Select two nodes to compare their hierarchical relationships.
   - The nodes are highlighted in the graph for easy comparison.

## Modules

- **`main.py`**: The entry point of the application that initializes the Streamlit app and coordinates between different modules.
- **`layout.py`**: Contains functions to set up the layout and styling of the Streamlit interface.
- **`data_handler.py`**: Handles loading and processing of data from JSON files.
- **`networkx_plot.py`**: Contains the logic of handling user interactions for NetworkX plot.
- **`d3js_plot.py`**: Manages the D3.js plot data preparation.
- - **`networkx_template.html`**: Contains the logic for rendering the NetworkX plot.
- **`d3js_template.html`**: Manages the D3.js plot rendering.


## Contributing

We welcome contributions to enhance the functionality and usability of this tool. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b branch_name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin branch_name`).
5. Create a new Pull Request.

## Copyright

&copy;2024 , Made For <b>"UWA NLP-TLP Group"</b>, Designed and Developed by <b>Manish Varada Reddy, Melo Xue, Shanmugapriya Sankarraj, Xudong Ying, Yu Xia, Zihan Zhang</b>.
