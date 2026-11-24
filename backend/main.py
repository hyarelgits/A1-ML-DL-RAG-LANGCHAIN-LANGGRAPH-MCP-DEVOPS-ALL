from fastapi import FastAPI
# # fastapi = Backend framework, FastAPI = Class to make app
from fastapi.middleware.cors import CORSMiddleware
# # CORSMiddleware = Allow React (3000) to talk to FastAPI (8000), else browser blocks
import sqlite3
import pickle
# # sqlite3 = Database - No need to install, Python already has it
import os
# # os = Operating System - To get file path, join paths
from pydantic import BaseModel
# # pydantic = Data validation, BaseModel = Base class for input data

app = FastAPI(title="Security Incident AI")
# # app = Our FastAPI app object, title = Name shown in docs
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
# # add_middleware = Add CORS, allow_origins=["*"] = Allow all websites, allow_methods = Allow GET, POST, etc.

DB = os.path.join(os.path.dirname(__file__), "security.db")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
try:
    MODEL = pickle.load(open(MODEL_PATH, "rb"))
    print("Model loaded:", MODEL_PATH)
except Exception as e:
    MODEL = None
    print("Model not loaded, using rule:", e)
# # os.path.dirname(__file__) = Folder where main.py is - backend folder
# # os.path.join = Join folder + security.db = backend/security.db
# # FIXED - DB always inside backend, no "database not found" error

def init_db():
    # # def = Make function, init_db = Initialize Database
    con = sqlite3.connect(DB)
    # # sqlite3.connect(DB) = Connect to DB file, if not exists, create it
    con.execute("CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY, title TEXT, description TEXT, severity TEXT, source_ip TEXT, status TEXT, predicted_label TEXT, cluster INTEGER)")
    # # CREATE TABLE IF NOT EXISTS = Create table only if not already there
    # # incidents = Table name, id = Primary Key, title = Incident title, etc.
    con.execute("INSERT OR IGNORE INTO incidents VALUES (1,'Phishing Login','Fake login page','high','192.168.1.10','open','malware',0)")
    # # INSERT OR IGNORE = Insert only if id 1 not already there, else ignore - So no duplicate on restart
    con.execute("INSERT OR IGNORE INTO incidents VALUES (2,'Brute Force','Many login fails','medium','10.0.0.5','open','bruteforce',1)")
    # # Second sample incident - Brute Force
    con.execute("INSERT OR IGNORE INTO incidents VALUES (3,'SQL Injection','OR 1=1 in URL','critical','172.16.0.2','open','injection',0)")
    # # Third sample incident - SQL Injection
    con.commit()
    # # commit = Save changes to DB file
    con.close()
    # # close = Close DB connection

init_db()
# # Call init_db - Run function now, so DB + table + 3 incidents created

class Incident(BaseModel):
    # # class Incident = What data we take from user, BaseModel = Pydantic base
    title: str
    # # title: str = Title must be text
    description: str
    # # description: str = Description must be text
    severity: str
    # # severity: str = Severity must be text - high/medium/critical
    source_ip: str
    # # source_ip: str = IP must be text
@app.get("/")
# # @app.get("/") = When user opens http://localhost:8000/, run home()
def home():
    # # def home = Function for home page
    return {"message": "Security Incident AI Running"}
    # # return = Send back JSON message - Backend is running

@app.get("/incidents")
# # @app.get("/incidents") = When user opens /incidents, run list_incidents()
def list_incidents():
    # # def list_incidents = Show all incidents
    con = sqlite3.connect(DB)
    # # Connect to DB
    con.row_factory = sqlite3.Row
    # # row_factory = Return rows as dict-like, so we can convert to JSON
    rows = [dict(r) for r in con.execute("SELECT * FROM incidents")]
    # # SELECT * = Select all columns, from incidents table, dict(r) = Convert each row to dict
    con.close()
    # # Close DB
    return rows
    # # Return list of incidents

@app.post("/incidents")
# # @app.post("/incidents") = When user sends POST to /incidents, run create_incident()
def create_incident(data: Incident):
    # # data: Incident = Input data must match Incident class - title, description, etc.
    label = "malware" if "login" in data.description.lower() else "anomaly"
    # # label = If description has word "login", label = malware, else anomaly - Simple Supervised rule for demo
    cluster = 1 if data.severity in ["high", "critical"] else 0
    # # cluster = If severity is high or critical, cluster = 1 (High group), else 0 (Low group) - K-Means idea
    con = sqlite3.connect(DB)
    # # Connect to DB
    con.execute("INSERT INTO incidents (title,description,severity,source_ip,status,predicted_label,cluster) VALUES (?,?,?,?,?,?,?)", (data.title, data.description, data.severity, data.source_ip, "open", label, cluster))
    # # INSERT INTO = Add new row, ? = Placeholder, values in tuple - Prevents SQL Injection
    con.commit()
    # # Save
    con.close()
    # # Close
    return {"status": "created", "predicted_label": label, "cluster": cluster}
    # # Return success + predicted label + cluster

@app.get("/predict/{text}")
# # @app.get("/predict/{text}") = When user opens /predict/anything, text = anything
def predict(text: str):
    # # def predict = Predict for one text
    label = "malware" if "login" in text.lower() else "anomaly"
    # # Same rule - If text has login, malware, else anomaly
    return {"text": text, "predicted_label": label}
    # # Return text + label

@app.get("/rag/{question}")
# # @app.get("/rag/{question}") = When user asks question, run rag()
def rag(question: str):
    # # def rag = RAG answer function
    return {"question": question, "answer": f"Retrieved from ChromaDB: Similar incident found for '{question}'. Suggested action: Block IP, Reset password, Check logs in Jenkins."}
    # # Return question + fake RAG answer for now - In Step 10 we make it real ChromaDB
