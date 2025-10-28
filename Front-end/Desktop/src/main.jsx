import React from "react"
import ReactDOM from "react-dom/client"
import ChatBubble from "./components/ChatBubble/ChatBubble.jsx"

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ChatBubble/>
  </React.StrictMode>,
);

import './components/ChatBubble/main.js';