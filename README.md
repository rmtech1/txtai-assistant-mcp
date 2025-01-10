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
