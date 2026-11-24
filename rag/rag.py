# Step 5 - RAG + ChromaDB + LangChain + LangGraph + MCP
# RAG = Retrieval Augmented Generation
# ChromaDB = Vector Database - Stores docs as vectors
# LangChain = Chain to retrieve + answer
# LangGraph = Decision - If critical -> Escalate, else Suggest
# MCP = Tools - block_ip, check_logs, send_alert

import chromadb
# # chromadb = Vector DB library

print("RAG Started...")
# # Print start

client = chromadb.Client()
# # client = ChromaDB client, Client() = In-memory client for learning
col = client.get_or_create_collection("incidents")
# # get_or_create_collection("incidents") = Get collection if exists, else create new
# # incidents = Collection name, like table name

try:
    col.delete(ids=["1", "2", "3"])
    # # delete = Delete old docs with ids 1,2,3 - So no duplicate on re-run
except:
    pass
    # # pass = If delete fails (no docs), do nothing, continue
    # # try/except = Try delete, if error, don't stop, just pass

col.add(
    # # col.add = Add docs to ChromaDB
    documents=[
        "Phishing login fake page - User clicked fake login link, password stolen",
        # # Doc 1 - Phishing
        "Brute force many login fails - Attacker tried many passwords on admin login",
        # # Doc 2 - Brute Force
        "SQL Injection OR 1=1 in URL - Attacker injected SQL in website URL"
        # # Doc 3 - SQL Injection
    ],
    ids=["1", "2", "3"]
    # # ids = Unique IDs for docs - 1,2,3
)
print("ChromaDB - 3 docs added")
# # Print docs added

def retrieve(question):
    # # def retrieve = Function to search ChromaDB, question = User question
    res = col.query(query_texts=[question], n_results=1)
    # # col.query = Search, query_texts=[question] = Search for question, n_results=1 = Get top 1 best match
    return res['documents'][0][0]
    # # return = First doc, first result - Best match

def decide(question, retrieved_doc):
    # # def decide = LangGraph decision, question = User question, retrieved_doc = Found doc
    if "critical" in question.lower() or "sql" in question.lower() or "injection" in question.lower():
        # # if = If question has critical or sql or injection words
        # # question.lower() = Make lowercase, so "SQL" and "sql" both match
        return "ESCALATE - Call Senior Team"
        # # return Escalate - Critical case
    else:
        # # else = If not critical
        return "SUGGEST - Block IP, Reset Password"
        # # return Suggest - Normal case

def mcp_tools(action):
    # # def mcp_tools = MCP Tools, action = Decision from decide()
    if action == "ESCALATE - Call Senior Team":
        # # if action is Escalate
        return "MCP Tools Used: send_alert + check_logs"
        # # return tools for Escalate - Send alert + Check logs
    else:
        # # else = Suggest case
        return "MCP Tools Used: block_ip + check_logs"
        # # return tools for Suggest - Block IP + Check logs

def ask(question):
    # # def ask = Full RAG flow, question = User question
    doc = retrieve(question)
    # # doc = Retrieve step - Find similar old incident
    decision = decide(question, doc)
    # # decision = Decide step - Escalate or Suggest
    tools = mcp_tools(decision)
    # # tools = MCP step - Which tools to use
    answer = f"Retrieved: {doc} | Decision: {decision} | {tools}"
    # # answer = Combine all - Retrieved + Decision + Tools
    return answer
    # # return answer

print("Test 1:", ask("fake login page"))
# # Test 1 - Ask about fake login - Should retrieve Phishing doc
print("Test 2:", ask("SQL injection critical"))
# # Test 2 - Ask about SQL - Should retrieve SQL doc + Escalate
print("RAG Done - All Working")
# # Print done
