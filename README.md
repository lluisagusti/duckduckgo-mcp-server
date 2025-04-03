# Ollama MCP Server

A Model Context Protocol (MCP) server that provides a complete interface to Ollama commands, allowing you to manage and run large language models through Ollama.

## Features

- **Complete Ollama Command Support**: Implements all major Ollama commands
- **Model Management**: Create, show, run, stop, pull, push, list, and remove models
- **Async Implementation**: Built with async/await for optimal performance
- **Error Handling**: Comprehensive error handling and logging
- **Environment Configuration**: Configurable Ollama API endpoint

## Installation

### Installing via `uv`

Install directly from PyPI using `uv`:

```bash
uv pip install ollama-mcp-server
```

### Development Installation

For local development:

```bash
git clone https://github.com/yourusername/ollama-mcp-server
cd ollama-mcp-server
uv pip install -e .
```

## Configuration

The server uses the following environment variables:

- `OLLAMA_API_URL`: The URL of your Ollama API (default: `http://localhost:11434`)

## Usage

### Running with Claude Desktop

1. Download [Claude Desktop](https://claude.ai/download)
2. Create or edit your Claude Desktop configuration:
   - On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

```json
{
    "mcpServers": {
        "ollama": {
            "command": "uvx",
            "args": ["ollama-mcp-server"]
        }
    }
}
```

3. Restart Claude Desktop

### Available Commands

- `create`: Create a model from a Modelfile
- `show`: Show information for a model
- `run`: Run a model
- `stop`: Stop a running model
- `pull`: Pull a model from a registry
- `push`: Push a model to a registry
- `list`: List models
- `ps`: List running models
- `cp`: Copy a model
- `rm`: Remove a model

### Example Modelfile

```
FROM gemma:7b
SYSTEM "You will always respond in correct and natural English. You are a helpful and friendly assistant."
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER stop "User:"
PARAMETER stop "Assistant:"
PARAMETER num_ctx 2048
PARAMETER repeat_penalty 1.1
PARAMETER num_gpu 1
LICENSE "CC BY-NC-SA 4.0"
```

## Development

For local development, you can use the MCP CLI:

```bash
# Run with the MCP Inspector
mcp dev server.py

# Install locally for testing with Claude Desktop
mcp install server.py
```

## Contributing

Issues and pull requests are welcome! Some areas for potential improvement:

- Additional parameter validation
- Enhanced error handling
- Caching layer for frequently used models
- Support for advanced Ollama features

## License

This project is licensed under the MIT License.