## Aviationstack MCP

Aviationstack MCP is a Model Context Protocol (MCP) server for the Aviationstack API to interact with Live Flight Data. 

### Features
- Get Flight data for a specific Airline.
- Get Flight data departing from a specific airport.

### Prerequisites

- Aviationstack API Key (You can get a FREE API Key from [Aviationstack](https://aviationstack.com/signup/free))
- Python 3.10 or newer
- uv package manager: 

### MCP Server configuration

```json
{
  "mcpServers": {
    "Aviationstack MCP": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli],requests",
        "mcp",
        "run",
        "/path/to/your/server.py"
      ],
      "env": {
        "AVIATION_STACK_API_KEY": "<your-api-key>"
      }
    }
  }
}
