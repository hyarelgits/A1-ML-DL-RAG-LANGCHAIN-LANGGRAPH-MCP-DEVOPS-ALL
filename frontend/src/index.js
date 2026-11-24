import React from "react";
// # import React
import ReactDOM from "react-dom/client";
// # import ReactDOM - To show React in browser
import App from "./App";
// # import App - Our App.jsx

const root = ReactDOM.createRoot(document.getElementById("root"));
// # root = Find HTML element with id="root", createRoot = Make React root there
root.render(<App />);
 // # root.render(<App />) = Show App inside root
