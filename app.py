import streamlit as st
from falkordb import FalkorDB
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(page_title="Graph Hacks - FalkorDB Explorer", layout="wide")

st.title("🌐 FalkorDB Knowledge Graph Explorer")
st.write("Context-aware Graph Visualization for AI Agents")

# Database Connection
db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('CompanyBrain')

# Tab Layout
tab1, tab2 = st.tabs(["📊 Interactive Graph View", "➕ Add New Context"])

with tab1:
    st.subheader("Live Graph Search & Visualization")
    cypher_query = st.text_input("Cypher Query:", "MATCH (p:Person)-[r]->(n) RETURN p.name, type(r), labels(n)[0], coalesce(n.name, n.risk)")

    if st.button("Run Graph Query"):
        try:
            result = graph.query(cypher_query)
            
            nodes = []
            edges = []
            node_set = set()

            for row in result.result_set:
                source, rel, target_type, target = row[0], row[1], row[2], row[3]

                # Create Source Node
                if source not in node_set:
                    nodes.append(Node(id=source, label=source, color="#4CAF50"))
                    node_set.add(source)

                # Create Target Node
                target_id = f"{target_type}:{target}"
                if target_id not in node_set:
                    nodes.append(Node(id=target_id, label=target, color="#2196F3"))
                    node_set.add(target_id)

                # Create Edge
                edges.append(Edge(source=source, target=target_id, label=rel))

            st.write("### Graph Connections:")
            config = Config(width=800, height=450, directed=True, physics=True)
            agraph(nodes=nodes, edges=edges, config=config)

        except Exception as e:
            st.error(f"Error executing query: {e}")

with tab2:
    st.subheader("Inject Context into FalkorDB")
    with st.form("add_node_form"):
        person_name = st.text_input("Person Name")
        role = st.text_input("Role")
        project_name = st.text_input("Project Name")
        submitted = st.form_submit_button("Add Node to Graph")

        if submitted and person_name and project_name:
            ingest_query = f"""
            MERGE (p:Person {{name: '{person_name}', role: '{role}'}})
            MERGE (proj:Project {{name: '{project_name}'}})
            MERGE (p)-[:WORKS_ON]->(proj)
            """
            graph.query(ingest_query)
            st.success(f"Added connection: {person_name} -> WORKS_ON -> {project_name}")