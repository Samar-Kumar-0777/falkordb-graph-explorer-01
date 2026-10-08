import os
from dotenv import load_dotenv
from falkordb import FalkorDB
load_dotenv()
db = FalkorDB(host=os.getenv("FALKORDB_HOST", "localhost"), port=int(os.getenv("FALKORDB_PORT", 6379)))
graph = db.select_graph("CompanyBrain")
setup_query = """
CREATE 
  (p1:Person {name: 'Samar', role: 'Developer'}),
  (p2:Person {name: 'Alex', role: 'Security Analyst'}),
  (proj:Project {name: 'React SaaS', status: 'Active'}),
  (sys:System {name: 'Auth Module', risk: 'High'}),
  (p1)-[:WORKS_ON]->(proj),
  (p2)-[:AUDITS]->(sys),
  (proj)-[:DEPENDS_ON]->(sys)
"""
graph.query(setup_query)
print("Success! FalkorDB mein Knowledge Graph ban gaya hai.")
