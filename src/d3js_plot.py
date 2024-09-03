import streamlit as st
import streamlit.components.v1 as components
import json
import os

def display_d3js_plot(data, search_term, parent_limit, children_limit):
    """Display the D3.js plot using the HTML template."""
    st.header("D3.js Plot")

    hierarchical_data = prepare_hierarchical_data(data, search_term, parent_limit, children_limit)
    hierarchical_data_json = json.dumps(hierarchical_data)

    with open("../static/d3_plot.html", "r") as f:
        d3_template = f.read()

    d3_html = d3_template.replace("{{data}}", hierarchical_data_json)
    d3_html = d3_html.replace("{{width}}", "1200")  
    d3_html = d3_html.replace("{{height}}", "1000")

    components.html(d3_html, height=1000)

def prepare_hierarchical_data(data, search_term, parent_limit, children_limit):
    """Prepare hierarchical data for D3.js visualization."""
    def get_color_by_level(level):
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
        return colors[level % len(colors)]

    def get_specific_node_color(node_name):
        if node_name == "Superclasses":
            return "#FFD700"
        elif node_name == "Subclasses":
            return "#1E90FF"
        else:
            return None

    def find_parents(node_name, level, data, current_level=1):
        if level == 0:
            return []
        parents = []
        for item in data:
            if node_name in item["subclasses"].split(", "):
                color = get_specific_node_color(item["uniqueName"]) or get_color_by_level(current_level)
                parents.append({
                    "name": item["uniqueName"],
                    "children": find_parents(item["uniqueName"], level - 1, data, current_level + 1),
                    "color": color,
                    "description": item["description"]
                })
        return parents

    def find_children(node_name, level, data, current_level=1):
        if level == 0:
            return []
        children = []
        for item in data:
            if node_name in item["superclasses"].split(", "):
                color = get_specific_node_color(item["uniqueName"]) or get_color_by_level(current_level)
                children.append({
                    "name": item["uniqueName"],
                    "children": find_children(item["uniqueName"], level - 1, data, current_level + 1),
                    "color": color,
                    "description": item["description"]
                })
        return children

    filtered_data = [item for item in data if item["uniqueName"] == search_term][0]
    hierarchical_data = {
        "name": filtered_data["uniqueName"],
        "children": [
            {
                "name": "Superclasses",
                "children": find_parents(filtered_data["uniqueName"], parent_limit, data),
                "color": get_specific_node_color("Superclasses")
            },
            {
                "name": "Subclasses",
                "children": find_children(filtered_data["uniqueName"], children_limit, data),
                "color": get_specific_node_color("Subclasses")
            }
        ],
        "color": "red",
        "description": filtered_data["description"]
    }

    return hierarchical_data