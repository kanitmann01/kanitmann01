# MCP Server - kanitmann01 Profile

A [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes structured data about Kanit Mann's projects, skills, and experience for AI assistants to query.

## Setup

```bash
pip install -r mcp_server/requirements.txt
```

## Running the Server

```bash
python -m mcp_server.server
```

The server communicates over stdio using the MCP protocol.

## Available Tools

| Tool | Description |
|------|-------------|
| `projects` | Returns featured projects (Brand Guard, kanit.codes) with descriptions, tech stacks, and links |
| `skills` | Returns categorized tech stack (Languages, ML & Data Science, Data Platforms & Cloud, Visualization & BI, Techniques) |
| `experience` | Returns work history (NetSTAR ML Engineer, Ericsson Cloud/Infra Engineer) with details and achievements |

## Testing

```bash
python -m pytest mcp_server/tests/test_server.py -v
```

## MCP Client Configuration

Add to your MCP client config (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "kanitmann01": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "path/to/kanitmann01"
    }
  }
}
```
