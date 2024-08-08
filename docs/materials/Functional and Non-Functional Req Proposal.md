# ISO 15926-4 Interactive Visualization Project.

**CITS5206 TEAM-18**

**August 2024**

# 1 Aim

The aim of this project is to develop an interactive visualization tool for an equipment reference data library described in the ISO 15926-4 Standard. This tool will allow members of the ISO TC 184 SC4 committee, including Prof. Melinda Hodkiewicz, to efficiently interrogate and visualize hierarchical data relationships through a web-based interface. The tool is intended to be demoed at the ISO meeting in Stavanger, Norway, in late October.

# 2 Base Case

Currently, members of the ISO TC 184 SC4 committee have to manually search through extensive data records to find relevant information. This process is time-consuming and inefficient, as it involves navigating through large datasets without an intuitive interface to highlight hierarchical relationships.

# 3 Proposed Solution

The proposed solution is to create a web-based interface that integrates with the data available at the SPARQL endpoint ([https://data.15926.org/sparql](https://data.15926.org/sparql)). Using this interface, users will be able to query the database and visualize the hierarchical relations of the equipment reference data. The visualization tool will be developed using Streamlit, but we remain open to alternative frameworks based on project needs and client preferences.

# 4 Functionality

Our website will consist of the following main pages:

**Search and Visualization:** Users can enter their queries in a search bar and visualize the hierarchical relations in the data. The page will provide various interactive elements to filter, search, and navigate through the data. Both parent branches and child branches of the hierarchy can be expanded and collapsed for detailed viewing.

# 5 System Design

There are a number of factors to consider when deciding a stack, shown in the following table:

| Factor | Priority | Explanation |
| --- | --- | --- |
| Project requirements | Highest | The stack must be capable of fulfilling all requirements. |
| Continued development | High | The stack must use familiar technologies that are well-known and industry-standard. |
| Skills and backgrounds | High | Due to the short time frame, picking technologies where all developers are comfortable is important. |
| Languages’ ecosystems | High | The language must have libraries capable of fulfilling the requirements. |
| Guides and documentation | Medium  | The existence of detailed guides and documentation is important, and directly relates to using familiar technology. |
| Library ease-of-use | Medium | The libraries chosen should have a good developer experience and interface well with one another. |
| Learning curve | Low | While desirable, this is unavoidable and hard to evaluate as members do not have prior experience which addresses all aspects of the project’s requirements. |

The project will be built as a web application, organized into a single framework using Streamlit. Streamlit will handle both the frontend interface and backend data interactions with the SPARQL endpoint.

- **Backend:** SPARQL
- **Frontend:** Streamlit
- **Deployment:** Amazon AWS

### Backend — SPARQL

The project will use SPARQL to query the equipment reference data stored at the provided endpoint. The SPARQL queries will retrieve data dynamically based on user input, allowing for interactive and responsive data visualization.

### Frontend — Streamlit

We propose using Streamlit for the frontend to create an interactive web-based interface. Streamlit allows for rapid development of data applications with Python, integrating seamlessly with SPARQL for backend data retrieval.

### Key Features:

- **Search Bar:** Users can enter queries to search the hierarchical data.
- **Data Visualization:** Display hierarchical data with expandable parent and child branches.
- **User Interaction:** Users can filter, search, and navigate through the data interactively.

# 6 Requirements

### **Functional Requirements**

### Data Interaction

| Identifier | Name | Description |
| --- | --- | --- |
| FR1.1 | Query Input | Users should be able to input a hierarchy into the search bar. |
| FR1.2 | Data Retrieval | The system should return relevant information from the SPARQL endpoint based on user queries. |
| FR1.3 | Visualization | The system should provide a visual representation of hierarchical data, with expandable and collapsible parent and child branches. |

### **Non-Functional Requirements**

### Performance

| Identifier | Name | Description |
| --- | --- | --- |
| NFR1.1 | Defined Time | The system should return query responses within a defined time frame (e.g., within 3 seconds). |

### Maintainability

| Identifier | Name | Description |
| --- | --- | --- |
| NFR2.1 | Clear Code | The codebase should be well-documented, formatted, and linted to facilitate future updates and maintenance. |

### Compatibility

| Identifier | Name | Description |
| --- | --- | --- |
| NFR3.1 | SPARQL Integration | The application should interface seamlessly with the SPARQL endpoint for data retrieval. |
| NFR3.2 | Responsive Design | The application design should support both desktop and mobile views. |

# 7 Risk Register

The risk register aims to include as many plausible dangers as possible. With that, it includes a variety of mitigation strategies for each risk. As a team, we have endeavoured to include as many of these mitigation strategies in the form of either functional or non-functional requirements (previously stated). Strategies that are not included in our list of requirements shall be viewed as helpful strategies for MRIWA and future development teams on this project. An example is having training sessions for employees utilising the systems – something that our group cannot satisfy, but a suggestion nonetheless, and one that can be informed by user manuals/resources which our team can provide.

|  | Uncontrolled |  |  |  | Controlled |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Potential Danger (Provide detail) | Likelihood | Consequence | Risk Rating | Controls = Actions which can lower the Risk | Likelihood | Consequence | New Risk Rating |
| Data Breach (Unintended release or access to client’s internal PDFs) | Unlikely | Extreme | Major (Maj4) | - Encrypted connection for data transfers
- Only utilize vetted open-source tools
- Periodically review security updates | Rare | Moderate | Minor (Mi5) |
| Inaccurate Retrieval (System not fetching relevant data from PDFs) | Possible | Major | Major (Maj2) | - Regular system tests using competency questions
- Devise further testing criterion
- Research | Unlikely | Moderate | Minor (Mi6) |
| Loss of Data during Processing | Rare | Extreme | Major (Maj3) | - Regular SharePoint back-ups
- Data integrity checks when moving/processing data | Rare | Moderate | Minor (Mi5) |
| Incompatibility Issues with Open-Source Tool(s) | Unlikely | Moderate | Minor (Mi6) | - Test tools for compatibility with client systems before full deployment
- Have alternatives in place | Rare | Moderate | Minor (Mi5) |
| Poor System Performance (slow response times) | Possible | Moderate | Moderate (Mo2) | - Utilise metrics and regularly measure
- Optimise data processing and retrieval processes | Unlikely | Minor | Low (L5) |
| Inadequate Access Control (unauthorised personnel accessing the system) | Possible | Major | Major (Maj2) | - Role-based access control
- Authentication system
- Access logging/tracking activity (added benefit for later debugging) | Unlikely | Major | Moderate (Mo5) |
| Over-reliance on Open-Source Tools (tools might become deprecated or unsupported) | Possible | Moderate | Moderate (Mo2) | - Regularly review and update open-source tools
- Have plans/backup tools in place | Rare | Moderate | Minor (Mi5) |
| Insufficient Logging and Monitoring (hinders tracing issues or user behaviour) | Unlikely | Moderate | Minor (Mi6) | - Implement comprehensive logic and monitoring from the outset
- Possibly utilise tools that offer real-time monitoring | Rare | Moderate | Minor (Mi5) |
| Scalability Concerns (system cannot handle more users/queries than anticipated) | Possible | Major | Major (Maj2) | Design system with scalability in mind,
and well documented to make future scaling smoother | Possible | Minor | Minor (Mi3) |
| Inadequate User Training (users unfamiliar with querying the system) | Likely | Moderate | Moderate (Mo3) | -User manuals and help resources
-Training sessions | Rare | Minor | Low (L4) |
| Inefficient Error Handling (leads to crashes or unclear messages) | Possible | Moderate | Moderate (Mo2) | - Implement comprehensive error handling
- Test and refine based on feedback and competency tests | Rare | Minor | Low (L4) |
| Unanticipated Costs | Possible | Moderate | Moderate (Mo2) | - Budget reviews
- Allocate a contingency budget | Unlikely | Minor | Low (L5) |
| Data Storage Limitations | Possible | Major | Major (Maj2) | - Monitor storage usage
- Use scalable storage solutions | Unlikely | Major | Moderate (Mo5) |
| Security Vulnerabilities (in third-party tools) | Unlikely | Extreme | Major (Maj4) | - Regularly update libraries
- Vulnerability scanners
- Security audits | Rare | Major | Moderate (Mo4) |

# 8 User Acceptance Tests

The goal of the UAT is to validate the functionality, usability, and reliability of the interactive visualization tool for the ISO 15926-4 equipment reference data library. The UAT will involve committee members interacting with the tool to ensure it meets their needs for querying and visualizing data relationships efficiently. The following are the provided competency questions:
### Test Cases

### Test Case 1: Access the Web Interface: Ensure users can access the web interface without issues.

1. Open a web browser.
2. Navigate to the URL of the visualization tool.

**Expected Results**: The web interface loads successfully without errors.

### Test Case 2: Query the Database: Verify that users can submit queries to the SPARQL endpoint.

1. Open the query input section on the web interface.
2. Enter a valid SPARQL query for equipment reference data.
3. Submit the query.

**Expected Results**: The query executes successfully, and results are displayed in the interface.

### Test Case 3: Visualize Hierarchical Relationships: Ensure that hierarchical data relationships are accurately visualized.

1. Execute a query that retrieves hierarchical relationships.
2. View the visualization of the results.

**Expected Results**: The hierarchical relationships are clearly and accurately displayed, showing nodes and connections.

### Test Case 4: Filter Data: Ensure users can apply filters to narrow down the visualization results.

1. Access the filtering options on the interface.
2. Apply filters based on specific criteria (e.g., equipment type, date).

**Expected Results**: The visualization updates to reflect only the filtered data, removing nodes that don't meet the criteria.
