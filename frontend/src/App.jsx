import React, { useEffect, useState } from "react";

export default function App() {
  const [incidents, setIncidents] = useState([]);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [severity, setSeverity] = useState("high");
  const [ip, setIp] = useState("");
  const [question, setQuestion] = useState("");
  const [ragAns, setRagAns] = useState("");

  const load = () => {
  fetch("http://127.0.0.1:8000/incidents")
    .then((r) => r.json())
    .then((data) => {
      console.log("DATA FROM API:", data);
      setIncidents(data);
    })
    .catch((e) => console.log("Backend not running", e));
};

  useEffect(() => {
    load();
  }, []);

  const submit = async () => {
    await fetch("http://localhost:8000/incidents", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        description: desc,
        severity,
        source_ip: ip,
      }),
    });

    load();
  };

  const ask = async () => {
    const r = await fetch(
      `http://localhost:8000/rag/${encodeURIComponent(question)}`
    ).then((r) => r.json());

    setRagAns(r.answer);
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Security Incident Portal</h1>

      <h2>Report Incident</h2>

      <input
        placeholder="Title"
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        placeholder="Description"
        onChange={(e) => setDesc(e.target.value)}
      />

      <input
        placeholder="Severity high/medium/critical"
        onChange={(e) => setSeverity(e.target.value)}
      />

      <input
        placeholder="Source IP"
        onChange={(e) => setIp(e.target.value)}
      />

      <button onClick={submit}>Submit</button>

      <h2>Incidents - SQLite + AI</h2>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Severity</th>
            <th>IP</th>
            <th>Predicted</th>
            <th>Cluster</th>
          </tr>
        </thead>

        <tbody>
          {incidents.map((i) => (
            <tr key={i.id}>
              <td>{i.id}</td>
              <td>{i.title}</td>
              <td>{i.severity}</td>
              <td>{i.source_ip}</td>
              <td>{i.predicted_label}</td>
              <td>{i.cluster}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Ask AI - RAG + LangChain + LangGraph + MCP</h2>

      <input
        placeholder="Ask about incident - e.g. fake login"
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={ask}>Ask</button>

      <p>{ragAns}</p>

      <p>
        Monitoring: Prometheus + Grafana | Logs: Jenkins | Deploy:
        Docker + K8s + Helm + Argo CD
      </p>
    </div>
  );
}
