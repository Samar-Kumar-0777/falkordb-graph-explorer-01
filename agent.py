import os
from dotenv import load_dotenv
from falkordb import FalkorDB
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
load_dotenv()
db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('CompanyBrain')
@tool
def query_knowledge_graph(cypher_query: str) -> str:
    """Execute a Cypher query on the FalkorDB graph database to fetch connected entity data."""
    try:
        result = graph.query(cypher_query)
        formatted_result = [str(row) for row in result.result_set]
        return "\n".join(formatted_result) if formatted_result else "No data found."
    except Exception as e:
        return f"Query Error: {str^(e)}"
tools = [query_knowledge_graph]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages( [
    ("system", "You are an AI assistant powered by FalkorDB. Graph Schema: Person, Project, System. Relationships: WORKS_ON, AUDITS, DEPENDS_ON. Always use query_knowledge_graph tool with valid Cypher query."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
] )
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
if __name__ == "__main__":
    query = "Kon Auth Module par kaam ya audit kar raha hai?"
    response = agent_executor.invoke( {"input": query} )
    print("\n--- Final Answer ---")
    print(response["output"])
