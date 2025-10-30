import React from "react";
import ReactDOM from "react-dom/client";
import ChatBubble from "./components/ChatBubble/ChatBubble.jsx";
import "./styles/global.css";

console.log("[main.jsx] carregado");
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ChatBubble />
  </React.StrictMode>
);
