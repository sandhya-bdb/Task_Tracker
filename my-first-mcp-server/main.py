# main.py
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from datetime import datetime

mcp = FastMCP("TaskTracker", json_response=True)

# ----------------------------
# Demo “database” / prefilled data
# ----------------------------
projects: Dict[str, Dict[str, Any]] = {
    "P001": {
        "name": "Website Redesign",
        "tasks": {
            "T001": {
                "title": "Design homepage UI",
                "status": "pending",
                "assignee": "U001",
                "comments": [
                    {"user": "U002", "comment": "Remember to follow brand colors", "time": "2025-11-30T10:15:00"}
                ]
            },
            "T002": {
                "title": "Implement login backend",
                "status": "in-progress",
                "assignee": "U003",
                "comments": []
            },
        }
    },
    "P002": {
        "name": "Marketing Campaign Nov-Dec",
        "tasks": {
            "T003": {
                "title": "Draft social media posts",
                "status": "completed",
                "assignee": "U004",
                "comments": [
                    {"user": "U004", "comment": "Initial draft done", "time": "2025-11-25T16:00:00"}
                ]
            }
        }
    }
}

tickets: Dict[str, Dict[str, Any]] = {
    "TK001": {
        "title": "Bug: login API returns error 500",
        "description": "When user tries to login with valid credentials, API crashes.",
        "reporter": "U003",
        "status": "open",
        "assignee": "U005",
        "comments": [
            {"user": "U005", "comment": "Looking into the stack trace", "time": "2025-11-30T11:45:00"}
        ]
    },
    "TK002": {
        "title": "Feature Request: Add \"Remember Me\" to login",
        "description": "User should stay logged in if they select remember-me option.",
        "reporter": "U002",
        "status": "in-review",
        "assignee": None,
        "comments": []
    }
}

users: Dict[str, Dict[str, str]] = {
    "U001": { "name": "Alice" },
    "U002": { "name": "Bob" },
    "U003": { "name": "Charlie" },
    "U004": { "name": "Diana" },
    "U005": { "name": "Eve" }
}

# ----------------------------
# Helper / ID-generator
# ----------------------------
def _gen_id(prefix: str) -> str:
    return f"{prefix}{int(datetime.now().timestamp()*1000)}"

# ----------------------------
# Project & Task Tools
# ----------------------------
@mcp.tool()
def list_projects() -> List[Dict[str, Any]]:
    return [ { "project_id": pid, "name": pdata["name"] } for pid, pdata in projects.items() ]

@mcp.tool()
def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    return projects.get(project_id)

@mcp.tool()
def create_project(name: str) -> str:
    pid = _gen_id("P")
    projects[pid] = { "name": name, "tasks": {} }
    return pid

@mcp.tool()
def add_task(project_id: str, title: str, assignee: str) -> Optional[str]:
    proj = projects.get(project_id)
    if not proj:
        return None
    tid = _gen_id("T")
    proj["tasks"][tid] = {
        "title": title,
        "status": "pending",
        "assignee": assignee,
        "comments": []
    }
    return tid

@mcp.tool()
def update_task_status(project_id: str, task_id: str, status: str) -> bool:
    proj = projects.get(project_id)
    if not proj or task_id not in proj["tasks"]:
        return False
    proj["tasks"][task_id]["status"] = status
    return True

@mcp.tool()
def add_task_comment(project_id: str, task_id: str, user: str, comment: str) -> bool:
    proj = projects.get(project_id)
    if not proj or task_id not in proj["tasks"]:
        return False
    proj["tasks"][task_id]["comments"].append({
        "user": user,
        "comment": comment,
        "time": datetime.now().isoformat()
    })
    return True

# ----------------------------
# Ticket / Issue Tools
# ----------------------------
@mcp.tool()
def list_tickets() -> List[Dict[str, Any]]:
    return [ { "ticket_id": tid, "title": t["title"], "status": t["status"] } for tid, t in tickets.items() ]

@mcp.tool()
def get_ticket(ticket_id: str) -> Optional[Dict[str, Any]]:
    return tickets.get(ticket_id)

@mcp.tool()
def create_ticket(title: str, description: str, reporter: str) -> str:
    tid = _gen_id("TK")
    tickets[tid] = {
        "title": title,
        "description": description,
        "reporter": reporter,
        "status": "open",
        "assignee": None,
        "comments": []
    }
    return tid

@mcp.tool()
def assign_ticket(ticket_id: str, assignee: str) -> bool:
    t = tickets.get(ticket_id)
    if not t:
        return False
    t["assignee"] = assignee
    return True

@mcp.tool()
def update_ticket_status(ticket_id: str, status: str) -> bool:
    t = tickets.get(ticket_id)
    if not t:
        return False
    t["status"] = status
    return True

@mcp.tool()
def add_ticket_comment(ticket_id: str, user: str, comment: str) -> bool:
    t = tickets.get(ticket_id)
    if not t:
        return False
    t["comments"].append({
        "user": user,
        "comment": comment,
        "time": datetime.now().isoformat()
    })
    return True

# ----------------------------
# Example resource: list of users
# ----------------------------
@mcp.resource("users://all")
def list_users() -> Dict[str, Dict[str, str]]:
    return users

# ----------------------------
# Example prompt templates for LLM interactions
# ----------------------------
@mcp.prompt()
def summary_of_project(project_id: str) -> str:
    """Generate a nice summary prompt for a project (tasks + statuses)."""
    proj = projects.get(project_id)
    if not proj:
        return f"Project with ID {project_id} not found."
    lines = [f"Project: {proj['name']} (ID: {project_id})", "Tasks:"]
    for tid, task in proj["tasks"].items():
        lines.append(f"- [{task['status']}] {task['title']} (ID: {tid}, Assignee: {task['assignee']})")
    return "\n".join(lines)

@mcp.prompt()
def ticket_details_prompt(ticket_id: str) -> str:
    """Generate a human-friendly prompt describing ticket details."""
    t = tickets.get(ticket_id)
    if not t:
        return f"Ticket with ID {ticket_id} not found."
    s = f"Ticket: {t['title']} (ID: {ticket_id})\n" \
        f"Status: {t['status']}\n" \
        f"Reporter: {t['reporter']}\n" \
        f"Assignee: {t.get('assignee')}\n" \
        f"Description: {t['description']}\n"
    if t['comments']:
        s += "Comments:\n"
        for c in t['comments']:
            s += f"- {c['user']} at {c['time']}: {c['comment']}\n"
    else:
        s += "No comments yet.\n"
    return s

# ----------------------------
# Run the server
# ----------------------------
if __name__ == "__main__":
    mcp.run()


