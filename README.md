# Project Name: Interactive Visualization Tool for Equipment Reference Data Libraries - Use case on 15926.org RDLs

This project is an interactive visualization tool for the 15926.org RDLs, designed to help users explore complex data relationships using NetworkX and D3.js visualizations. The application is built using Streamlit, providing an intuitive and interactive web interface.

## Table of Contents

- [Project Name: Interactive Visualization Tool for Equipment Reference Data Libraries - Use case on 15926.org RDLs](#project-name-interactive-visualization-tool-for-equipment-reference-data-libraries---use-case-on-15926org-rdls)
  - [Table of Contents](#table-of-contents)
  - [Data Retrieval](#data-retrieval)
  - [Installation](#installation)
    - [Mac/Linux:](#maclinux)
    - [Windows:](#windows)
  - [Running the Application After Initial Setup](#running-the-application-after-initial-setup)
    - [Mac/Linux:](#maclinux-1)
    - [Windows:](#windows-1)
  - [Filter Rule](#filter-rule)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [Modules](#modules)
  - [Troubleshooting](#troubleshooting)
  - [Run Testing Scripts](#run-testing-scripts)
  - [Contributing](#contributing)
  - [Copyright](#copyright)

## Data Retrieval

To retrieve the latest DATA from the ENDPOINT:

```bash
python3 scripts/data_retrieve.py
```
OR

```bash
python scripts/data_retrieve.py
```

## Installation

To run this project locally, follow these steps:

### Mac/Linux:
1. **Clone the Repository:**

   ```bash
   git clone https://github.com/nlp-tlp/15926-4-CITS5206-18.git
   cd 15926-4-CITS5206-18
   ```

2. **Set Up a Virtual Environment:**

   Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Check Installed Dependencies:**

   Use the provided script to check if all dependencies are installed properly:

   ```bash
   python3 scripts/plugin_check.py
   ```

5. **Run the Application:**

   ```bash
   streamlit run src/main.py
   ```

6. **Terminate the Application:**

   ```bash
   Control + C
   ```

7. **Exit the Virtual Environment** (when finished):

   ```bash
   deactivate
   ```

### Windows:
1. **Clone the Repository:**

   ```bash
   git clone https://github.com/nlp-tlp/15926-4-CITS5206-18.git
   cd 15926-4-CITS5206-18
   ```

2. **Set Up a Virtual Environment:**

   Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Required Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Check Installed Dependencies:**

   Use the provided script to check if all dependencies are installed properly:

   ```bash
   python scripts/plugin_check.py
   ```

5.	**(Optional) Install Watchdog for Better Performance:**
   For better performance, it is recommended to install the Watchdog module, which improves file monitoring. This requires the installation of Xcode command line tools (for macOS users):

   ```bash
   xcode-select --install
   pip install watchdog
   ```

6. **Run the Application:**

   ```bash
   streamlit run src/main.py
   ```

7. **Terminate the Application:**

   ```bash
   Control + C
   ```

8. **Exit the Virtual Environment** (when finished):

   ```bash
   deactivate
   ```

## Running the Application After Initial Setup

### Mac/Linux:
1. **Activate the Virtual Environment:**

   ```bash
   source venv/bin/activate
   ```

2. **Run the Application:**

   ```bash
   streamlit run src/main.py
   ```

3. **Exit the Virtual Environment** (when finished):

   ```bash
   deactivate
   ```

### Windows:
1. **Activate the Virtual Environment:**

   ```bash
   venv\Scripts\activate
   ```

2. **Run the Application:**

   ```bash
   streamlit run src\main.py
   ```

3. **Terminate the Application:**

   ```bash
   Control + C
   ```

4. **Exit the Virtual Environment**:

   ```bash
   deactivate
   ```

## Filter Rule

The filter rule used in the application is as follows:

- Data entries without **superclass**, **subclass**, **type**, and **description** will be excluded from the visualization.

This ensures that the visualized data maintains its integrity and relevance for exploring relationships within the ISO 15926-4 standard.

## Project Structure

```
data/
├── filtered_out_data.jason     # Data including invalid nodes
└── final_output.json           # Data source file
docs/
├── demos                       # Previous code
├── materials/                  # Unit materials
└── meeting_minutes/            # Recordings for each meeting.
scripts/
├── data_retrieve.py            # Script to update dataset from online source.
└── plugin_check.py             # Script to check installed dependencies
src/
├── main.py                     # Main application entry point
├── layout.py                   # Functions related to layout and styling
├── data_handler.py             # Data loading functions
├── networkx_plot.py            # NetworkX plot visualization functions
└── d3js_plot.py                # D3.js plot visualization functions
static/
└── images/
    └── nlp-tlp-logo.png
tests/
├── driverpath.py               # Driver path for testing
├── test_comp_view.py           # Test the comparative view
└── test.py                     # Test other functions
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
5. **Implemented Functions**:
   - **Click on a node**: When you click on a node, its 'Definition' and 'Type' are displayed in the sidebar.
   - **Mouse hover on a node**: Hovering over a node displays a floating window with the node's 'Definition' over it.
   - **Fullscreen mode**: Click the "Fullscreen" button to enable the fullscreen view of the model. Press "Esc" to exit fullscreen mode.
6. **Enable Comparative Analysis**:
   - Use the `Enable Comparative` button to enable the comparative analysis mode.
   - Select two nodes to compare their hierarchical relationships.
   - The nodes are highlighted in the graph for easy comparison.

## Modules

- **`main.py`**: The entry point of the application that initializes the Streamlit app and coordinates between different modules.
- **`layout.py`**: Contains functions to set up the layout and styling of the Streamlit interface.
- **`data_handler.py`**: Handles loading and processing of data from JSON files.
- **`networkx_plot.py`**: Contains the logic for handling user interactions for NetworkX plot.
- **`d3js_plot.py`**: Manages the D3.js plot data preparation and rendering.

## Troubleshooting

If the app does not run or you encounter issues, please follow these troubleshooting steps:

1. **Ensure the Virtual Environment is Activated**:
   If the dependencies are not recognized, make sure the virtual environment is activated by using the activation command mentioned above.
   
2. **Check for Dependency Issues**:
   Run the plugin check script to verify if all dependencies are installed:
   ```bash
   python3 scripts/plugin_check.py
   ```
   
3. **Reinstall Dependencies**:
   If any dependency is missing, you can install them individually using `pip install <dependency-name>`.
   

## Run Testing Scripts

Before running the test scripts, please complete the following steps:

1. **Download and Configure Chromedriver:**
   - Download the appropriate version of [Chromedriver](https://sites.google.com/chromium.org/driver/) based on your Chrome browser version.
   - Update the `driver_path` variable in `tests/driverpath.py` with the absolute path to the Chromedriver.

   - Example:
   ```python
   driver_path = "C:/Users/XXXX/Downloads/chromedriver-win64/chromedriver.exe"
   ```

2. **Set Application Port:**

   - The application port must be fixed to ensure the tests run correctly.
   - Use the following command to start the application on a specific port (e.g., 8501):
  
   ```bash
   streamlit run src/main.py --server.port 8501
   ```

3. **Run the test scripts**

   ```bash
   pytest tests/test.py
   pytest tests/test_comp_view.py
   ```


## Contributing

We welcome contributions to enhance the functionality and usability of this tool. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b branch_name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin branch_name`).
5. Create a new Pull Request.

## Copyright

&copy;2024 , Made For **"UWA NLP-TLP Group"**, Designed and Developed by **Manish Varada Reddy, Melo Xue, Shanmugapriya Sankarraj, Xudong Ying, Yu Xia, Zihan Zhang**.
