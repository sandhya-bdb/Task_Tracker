# TaskTracker — MCP Server + Claude Desktop Client

A simple **Task & Ticket Tracking** server built with FastMCP (Python), designed to work with a compatible MCP-client (e.g. Claude Desktop).  
This project lets you manage projects, tasks, tickets/issues and users — all via natural-language interaction or direct tool calls.

---

## 📄 Overview

TaskTracker exposes tools/resources via MCP so you can:

- List and inspect projects with IDs and names  
- Get details of a project (tasks, status, assignee, comments)  
- Create new projects  
- Add tasks to a project (with assignee)  
- Update task status and add comments  
- List and inspect tickets/issues  
- Create new tickets/issues  
- Assign tickets, update ticket status, add comments  
- List all users  

Note: Data storage is currently in-memory (Python dicts), ideal for demo, learning or small-scale use.

---

## 🚀 Features

- ✅ Projects & task management: create, list, update, comment  
- ✅ Ticket/issue tracking: create tickets, manage status, assign, comment  
- ✅ Simple, natural-language interface (via an LLM client using MCP)  
- ✅ Lightweight and easy to set up  

---

## 🧰 Tech Stack

- Language: Python 3.x  
- Server: FastMCP  
- Client: Claude Desktop (or any MCP-compatible client)  
- Data store: In-memory Python dictionaries  

---

## 📥 Installation & Setup

1. Clone or download the repository to your local machine  
2. (Optional) Create and activate a virtual environment  
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Linux/macOS
   # On Windows: venv\Scripts\activate
3. install dependencies
   ```bash
    pip install fastmcp
4. start the server
   ```bash
   python main.py
5. In Claude Desktop (or other MCP client), connect to the server and start using commands (tools/resources)
# 🧪 Example Prompts / Usage (via Claude Desktop)
  ```bash
List all projects.  
Show me the details of project P001.  
Create a new project "Mobile App Launch".  
Add a new task "Design landing page" under project P001 assigned to user U002.  
Update task T002 in project P001 to "completed".  

List all tickets.  
Create a ticket "Bug: logout not working", description "User cannot logout properly", reporter U004.  
Show details for ticket TK001.  
Assign ticket TK002 to user U005.  
Change status of ticket TK001 to "in-progress".  
Add a comment to ticket TK001 by user U005: "Started debugging the issue."  

List all users.
```

# 🛠 Future Improvements (What you can build next)

Persist data using a database (SQLite / PostgreSQL) instead of in-memory dicts

Add authentication/authorization if multiple users access

Develop a basic web UI or CLI interface for non-LLM clients

Add advanced features: task
