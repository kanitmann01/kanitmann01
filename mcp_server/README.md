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
| `availability` | Returns current job availability status, target roles, graduation date, and contact info |

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

### Cursor

Add to `.cursor/mcp.json` in your project:

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

### Docker-based client configuration

```json
{
  "mcpServers": {
    "kanitmann01": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "kanitmann01-mcp"]
    }
  }
}
```

## Docker Deployment

### Build and run

```bash
docker build -t kanitmann01-mcp .
docker run --rm -i kanitmann01-mcp
```

### Docker Compose

```bash
docker compose up --build
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_TRANSPORT` | `stdio` | Transport protocol (stdio or sse) |
| `MCP_HOST` | `0.0.0.0` | Host to bind to |
| `MCP_PORT` | `8080` | Port to listen on |

## Platform Deployment

### Render

1. Create a new Web Service pointing to this repo
2. Set build command: `pip install -r mcp_server/requirements.txt`
3. Set start command: `python -m mcp_server.server`
4. Set environment variable `MCP_TRANSPORT=sse`

### Railway

1. Create a new service from this repo
2. Railway auto-detects Python; set start command: `python -m mcp_server.server`
3. Add env vars: `MCP_TRANSPORT=sse`, `MCP_PORT=$PORT`

### GitHub Container Registry

```bash
docker build -t ghcr.io/kanitmann01/mcp-server:latest .
docker push ghcr.io/kanitmann01/mcp-server:latest
```
