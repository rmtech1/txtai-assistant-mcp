# TxtAI Assistant MCP

A Model Context Protocol (MCP) server implementation for semantic search and memory management using TxtAI. This server provides a robust API for storing, retrieving, and managing text-based memories with semantic search capabilities.

## Features

- 🔍 Semantic search across stored memories
- 💾 Persistent storage with file-based backend
- 🏷️ Tag-based memory organization and retrieval
- 📊 Memory statistics and health monitoring
- 🔄 Automatic data persistence
- 📝 Comprehensive logging
- 🔒 Configurable CORS settings
- 🤖 Integration with Claude and Cline AI

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- virtualenv (recommended)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/txtai-assistant-mcp.git
cd txtai-assistant-mcp
```

2. Run the start script:
```bash
./scripts/start.sh
```

The script will:
- Create a virtual environment
- Install required dependencies
- Set up necessary directories
- Create a configuration file from template
- Start the server

## Configuration

The server can be configured using environment variables in the `.env` file. A template is provided at `.env.template`:

```ini
# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
CORS_ORIGINS=*

# Logging Configuration
LOG_LEVEL=DEBUG

# Memory Configuration
MAX_MEMORIES=0
```

## Integration with Claude and Cline AI

This TxtAI Assistant can be used as an MCP server with Claude and Cline AI to enhance their capabilities with semantic memory and search functionality.

### Configuration for Claude

To use this server with Claude, add it to Claude's MCP configuration file (typically located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "txtai-assistant": {
      "command": "path/to/txtai-assistant-mcp/scripts/start.sh",
      "env": {}
    }
  }
}
```

### Configuration for Cline

To use with Cline, add the server configuration to Cline's MCP settings file (typically located at `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "txtai-assistant": {
      "command": "path/to/txtai-assistant-mcp/scripts/start.sh",
      "env": {}
    }
  }
}
```

### Available MCP Tools

Once configured, the following tools become available to Claude and Cline:

1. `store_memory`: Store new memory content with metadata and tags
```json
{
  "content": "Memory content to store",
  "metadata": {
    "source": "conversation",
    "timestamp": "2023-01-01T00:00:00Z"
  },
  "tags": ["important", "context"],
  "type": "conversation"
}
```

2. `retrieve_memory`: Retrieve memories based on semantic search
```json
{
  "query": "search query",
  "n_results": 5
}
```

3. `search_by_tag`: Search memories by tags
```json
{
  "tags": ["important", "context"]
}
```

4. `delete_memory`: Delete a specific memory by content hash
```json
{
  "content_hash": "hash_value"
}
```

5. `get_stats`: Get database statistics
```json
{}
```

6. `check_health`: Check database and embedding model health
```json
{}
```

### Usage Examples

In Claude or Cline, you can use these tools through the MCP protocol:

```python
# Store a memory
<use_mcp_tool>
<server_name>txtai-assistant</server_name>
<tool_name>store_memory</tool_name>
<arguments>
{
  "content": "Important information to remember",
  "tags": ["important"]
}
</arguments>
</use_mcp_tool>

# Retrieve memories
<use_mcp_tool>
<server_name>txtai-assistant</server_name>
<tool_name>retrieve_memory</tool_name>
<arguments>
{
  "query": "what was the important information?",
  "n_results": 5
}
</arguments>
</use_mcp_tool>
```

The AI will automatically use these tools to maintain context and retrieve relevant information during conversations.

## API Endpoints

### Store Memory
```http
POST /store
```
Store a new memory with optional metadata and tags.

**Request Body:**
```json
{
    "content": "Memory content to store",
    "metadata": {
        "source": "example",
        "timestamp": "2023-01-01T00:00:00Z"
    },
    "tags": ["example", "memory"],
    "type": "general"
}
```

### Search Memories
```http
POST /search
```
Search memories using semantic search.

**Request Body:**
```json
{
    "query": "search query",
    "n_results": 5,
    "similarity_threshold": 0.7
}
```

### Search by Tags
```http
POST /search_tags
```
Search memories by tags.

**Request Body:**
```json
{
    "tags": ["example", "memory"]
}
```

### Delete Memory
```http
DELETE /memory/{content_hash}
```
Delete a specific memory by its content hash.

### Get Statistics
```http
GET /stats
```
Get system statistics including memory counts and tag distribution.

### Health Check
```http
GET /health
```
Check the health status of the server.

## Directory Structure

```
txtai-assistant-mcp/
├── server/
│   ├── main.py           # Main server implementation
│   └── requirements.txt  # Python dependencies
├── scripts/
│   └── start.sh         # Server startup script
├── data/                # Data storage directory
├── logs/                # Log files directory
├── .env.template        # Environment configuration template
└── README.md           # This file
```

## Data Storage

Memories and tags are stored in JSON files in the `data` directory:
- `memories.json`: Contains all stored memories
- `tags.json`: Contains the tag index

## Logging

Logs are stored in the `logs` directory. The default log file is `server.log`.

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Error Handling

The server implements comprehensive error handling:
- Invalid requests return appropriate HTTP status codes
- Errors are logged with stack traces
- User-friendly error messages are returned in responses

## Security Considerations

- CORS settings are configurable via environment variables
- File paths are sanitized to prevent directory traversal
- Input validation is performed on all endpoints

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.
