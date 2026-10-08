from falkordb import FalkorDB

db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('CompanyBrain')

query = "MATCH (p:Person)-[r]->(n) RETURN p.name AS Person, type(r) AS Relation, labels(n)[0] AS Target_Type, coalesce(n.name, n.risk) AS Target_Name"
result = graph.query(query)

print("\n=== FALKORDB KNOWLEDGE GRAPH RESULT ===")
for row in result.result_set:
    print(f"{row[0]} -[{row[1]}]-> {row[2]}: {row[3]}")