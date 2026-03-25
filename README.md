# 🤖 AI Agent with MCP

An end-to-end implementation of an **AI Agent powered by MCP (Model Context Protocol)** that integrates external tools via an MCP server and executes intelligent workflows using LangChain / LangGraph.

---

## 🚀 Overview

This project demonstrates how to build a **tool-augmented AI agent** that:

- Connects to an MCP server over SSE
- Discovers and uses external tools dynamically
- Executes tool calls via LLM reasoning
- Returns structured and human-readable responses

---

## 🧩 Architecture
```bash
User Query
↓
AI Agent (MCPAgent)
↓
LLM (Gemini / other models)
↓
Tool Decision
↓
MCP Client
↓
MCP Server (MServer)
↓
External Tools (e.g., Web Search)
```

---

## 📦 Key Components

### 🔹 `MServer`
- MCP server implementation
- Exposes tools via MCP protocol
- Handles:
  - Tool registration
  - Tool execution
  - SSE-based communication

---

### 🔹 `MCPAgent`
- AI agent integrating LLM + MCP tools
- Responsibilities:
  - Connect to MCP server
  - Load available tools dynamically
  - Execute tool-calling workflow
  - Format final responses

---

## 🛠️ Features

- ✅ MCP (Model Context Protocol) integration
- ✅ SSE-based persistent communication
- ✅ Dynamic tool discovery
- ✅ Tool-calling AI agent
- ✅ Gemini / LLM support
- ✅ Async architecture
- ✅ Extensible tool framework

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/brij-joe/ai_agent_with_mcp.git
cd ai_agent_with_mcp
```

### 2. Create virtual environment
```bash
uv venv .venv
.venv\Scripts\activate   # Windows
```

### 3. Configure environment
```bash
Create a .env file: and copy your API key
GOOGLE_API_KEY=your_api_key
```

## ▶️ Running the Project
### 1. Start MCP Server
```bash
python src/start_mcp.py
```

### 2. Run AI Agent
```bash
python src/ask_agent.py
```

## 🧪 Example Query
Tell me top 10 news highlights today

## 🔧 Example Tools
🌐 Web Search (Tavily API)

📊 (Extendable for DB, APIs, etc.)

## 🧠 How It Works
Agent connects to MCP server via SSE

Loads available tools dynamically

User query is sent to LLM

LLM decides whether to call a tool

Tool executes via MCP server

Final response is generated and returned

## 📁 Project Structure
```bash
src/
│
├── agents/
│   └── mcp_agent.py       # MCPAgent implementation
├── agents/
│   └── mcp_agent.py       # MCP Server implementation
├── start_mcp.py           # MCP server (MServer)
├── ask_agent.py           # Entry point for agent queries
├── app_constants.py       # Configurations
```

## ⚠️ Known Challenges

SSE connection lifecycle management

Async stream handling

Tool execution synchronization

Model tool-calling reliability (depends on LLM)

## 🚀 Future Enhancements

🔄 Retry & resilience for MCP calls

🧠 Memory (vector DB integration)

🌐 Multi-tool orchestration

📡 Streaming responses

📊 Observability & tracing

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## 📜 License
MIT License

🙌 Acknowledgements

LangChain / LangGraph

MCP Protocol

Google Gemini API

---
## 📌 Notes 
This is not production-grade. It’s a simple demonstration of concepts. For deep dives into "Agentic AI System with MCP" design and architecture, feel free to reach out: 📧 brij_joe@yahoo.com

