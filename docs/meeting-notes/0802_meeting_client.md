# Meeting_Client_0802

| Meeting No: | 2 |
| --- | --- |
| Meeting Type: | Client |
| Date: | 02/08/24 |
| Time: | 12:00 - 13:00 |
| Place of Meeting: | [202C] EZONE |
| Other Participants |  Prof Hodkiewicz |

**Team Member:**

| Name | Student No. | Attendance |
| --- | --- | --- |
| Manish Varada Reddy | 23817492 | Yes |
| Melo Xue | 23955182 | Yes |
| Xudong Ying | 21938264 | Yes |
| Yu Xia | 24125299 | Yes |
| Zihan Zhang | 23956788 | Yes |

### **Client's Problem Statement and Objectives**

**Client's Goal:** Prof Melinda Hodkiewicz aims to create a web-based interactive visualization tool for the equipment reference data library described in the ISO 15926-4 Standard. The purpose of this tool is to enable users, including herself and other committee members, to easily navigate and interrogate the hierarchical data relationships within the library.

**Objectives:**

- **Data Accessibility:** The current data is stored in Excel files, which are often outdated and not dynamic. The goal is to use the SPARQL endpoint to pull the most up-to-date data directly.
- **Visual Hierarchy:** The visualization should represent the hierarchical nature of the data, allowing users to explore parent-child relationships within the dataset.
- **Interactivity:** Users should be able to interact with the visualization to expand and contract nodes, search for specific items, and view detailed information about each node.
- **Usability:** The tool should be intuitive and user-friendly, even for users with minimal technical skills.

### **Proposed Solution**

**Solution Description:**
We propose to develop a web-based application using the Streamlit framework (or an equivalent) to visualize the ISO 15926-4 Standard equipment reference data library. The application will feature an interactive hierarchical visualization, enabling users to explore the data dynamically.

**Key Features:**

- **Data Integration:** Use SPARQL queries to fetch the latest data from the provided endpoint.
- **Interactive Visualization:** Implement a dynamic, zoomable hierarchy using visualization libraries such as D3.js or similar.
- **Search Functionality:** Allow users to search for specific terms and navigate to their locations within the hierarchy.
- **User Controls:** Provide options to view different levels of the hierarchy, including superclasses and subclasses.

### **Functional Requirements**

1. **Data Retrieval:**
    - The system must be able to retrieve the latest data using SPARQL queries.
    - The system must pre-process the data into a format suitable for hierarchical visualization.
2. **Visualization:**
    - The visualization must display the hierarchical structure of the data.
    - Users must be able to interact with the visualization to expand or contract nodes.
    - The system must highlight specific nodes based on user input or search queries.
3. **User Interface:**
    - The interface must allow users to search for specific items.
    - The interface must provide controls to navigate through different levels of the hierarchy.
    - The system must be accessible and easy to use for users with minimal technical skills.
4. **Backend and Frontend:**
    - The backend should handle data retrieval and processing.
    - The frontend should display the interactive visualization and provide user controls.
    - Potential technologies include Streamlit, React, D3.js, and a suitable backend framework.

### **Non-Functional Requirements**

1. **Performance:**
    - The system must handle large datasets efficiently.
    - The visualization should respond quickly to user interactions.
2. **Scalability:**
    - The system should be designed to accommodate future expansions, such as additional data types or enhanced interaction features.
3. **Usability:**
    - The user interface should be intuitive and easy to navigate.
    - The system should provide clear feedback and instructions to users.
4. **Accessibility:**
    - The system should consider accessibility features, such as color contrast and screen reader compatibility.

### **Risk Register**

1. **Technical Risks:**
    - **Data Complexity:** The hierarchical data may be complex to visualize accurately.
    - **Performance Issues:** Large datasets may cause performance bottlenecks.
    - **Integration Challenges:** Ensuring seamless integration between SPARQL queries and the visualization.
2. **Project Risks:**
    - **Timeline Constraints:** Limited time to complete the project before the ISO meeting in October.
    - **Team Coordination:** Managing tasks and communication within a diverse team.
3. **Mitigation Strategies:**
    - **Incremental Development:** Implement and test features incrementally to identify and resolve issues early.
    - **Regular Client Meetings:** Maintain frequent communication with the client to ensure alignment on project goals and progress.
    - **Skill Assessment:** Conduct a skills audit within the team to allocate tasks effectively based on individual strengths.

### **User Stories and Acceptance Criteria**

1. **User Story 1:** As a committee member, I want to search for specific equipment terms so that I can quickly locate their details within the hierarchy.
    - **Acceptance Criteria:** The system must allow users to input search terms and navigate to the corresponding node in the visualization.
2. **User Story 2:** As a user, I want to expand and collapse nodes in the hierarchy to explore the relationships between different equipment types.
    - **Acceptance Criteria:** The visualization must provide controls to expand and collapse nodes dynamically.
3. **User Story 3:** As an engineer, I want to view detailed information about each node to understand its attributes and relationships.
    - **Acceptance Criteria:** The system must display detailed information about each node when selected.

### **Technical Specifications and Tools**

- **Backend:** Python, SPARQL for data retrieval.
- **Frontend:** Streamlit, D3.js for visualization.
- **Hosting:** DigitalOcean or AWS (to be set up and managed by the client).
- **Version Control:** GitHub for code repository and collaboration.
- **Communication:** Microsoft Teams for team communication and client interactions.

### **Next Steps**

1. **Initial Requirements Gathering:** Confirm the project scope and requirements with the client.
2. **Technical Research:** Investigate the tools and technologies to be used.
3. **Prototype Development:** Develop a basic prototype to demonstrate key functionalities.
4. **Client Feedback:** Present the prototype to the client and gather feedback.
5. **Iterative Development:** Implement the remaining features iteratively, with regular client reviews.