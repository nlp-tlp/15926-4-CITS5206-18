| **Meeting No:** | 6 |
| --- | --- |
| **Meeting Type:** | Team & Client |
| **Date:** | 16/08/24 |
| **Time:** | 10:00-13:00 |
| **Place of Meeting:** | [203] EZONE & System Health Lab |
| **Other Participants** |  Prof Hodkiewicz |

**Team Member:**

| **Name** | **Student No.** | **Attendance** |
| --- | --- | --- |
| Manish Varada Reddy | 23817492 | Yes |
| Melo Xue | 23955182 | Yes |
| Shanmugapriya Sankarraj | 23872782 | Yes |
| Xudong Ying | 21938264 | Yes |
| Yu Xia | 24125299 | Yes |
| Zihan Zhang | 23956788 | Yes |

### **Agenda:**

1. Review Deliverable 1 Report.
2. Discuss the current visualization model.

---

### **Discussion Points & Questions:**

1. **Search Functionality:**
    - Should the search function allow partial or complete match? Should it be case-sensitive?
    - **Response:** Search needs to support both partial matching and case insensitivity.
2. **Hierarchy vs Starnet Visualization:**
    - Should all nodes be displayed as a hierarchy or starnet? Should nodes on the same level be displayed in the same color?
    - **Response:** Yes, display as a hierarchy with uniform color for nodes at the same level.
3. **Data Loading:**
    - All data is loaded initially, which may take time, but it allows faster query response.
4. **Error Handling:**
    - What happens if an incorrect or non-existent name is inputted?
    - **Response:** Only search inside the list, and avoid loading the whole dataset again on incorrect inputs.
5. **Data Extraction:**
    - Should the app always extract up-to-date data from the ISO endpoint, or should it be done manually?
    - **Response:** Manually update the dataset.
6. **Display Node Levels:**
    - Should the app increase the number of children and parent nodes displayed (currently 10), or display all nodes within the inputted level?
    - **Response:** Limit display to levels up to 10.

---

### **Additional Points:**

1. **Auto-filling Search:** Implemented and completed (DONE).
2. **Preferred Visualization:**
    - Client prefers **NetworkX hierarchy** but is interested in seeing the D3.js tree visualization.
3. **Arrow Directions:** Arrow directions have been implemented (DONE).
4. **MVP Features:** Sidebar should display type and definition.
5. **Documentation:**
    - Stakeholders: ISO committee members (Users) and Professor Hodkiewicz (Owner/Maintainer).
    - Detailed documentation is needed for website maintenance.
6. **SPARQL Queries:** Include examples.
7. **Explore JSON format** for handling data.
8. **Documentation Reference:** Refer to “indeaav2” for documentation structure.
9. **Display Levels:** Ensure clarity in level-based displays.

---

### **Tasks for Next Meeting:**

- **Team A (Streamlit Visualization):** Continue improving the Streamlit visualization.
- **Team B (D3.js Visualization):** Work on D3.js visualization for hierarchical display.

---

### **Next Meeting Details:**

- **Date:** 20/08/2024, Tuesday
- **Time:** 14:00-16:00
- **Location:** Ezone North