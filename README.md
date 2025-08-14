# Shutter Timelock Encryption MCP Server

A Model Context Protocol (MCP) server that provides timelock encryption capabilities using the Shutter Network. This server allows users to encrypt messages that can only be decrypted after a specified future time, enabling trustless time-delayed communications.

## Features

- Timelock Encryption: Encrypt messages that unlock at future timestamps
- Natural Language Time Parsing: Use expressions like "3 months from now"
- Unix Timestamp Support: Direct timestamp input for precise timing
- Claude Web Integration: SSE protocol support for seamless Claude integration
- VS Code MCP Support: Compatible with VS Code MCP extensions
- Comprehensive Error Handling: User-friendly error messages and guidance
- Production Ready: Docker support, health checks, and monitoring

## Important Notice

**ALPHA SOFTWARE**: This is experimental software using the Shutter Network testnet deployment (Gnosis Chiado). Do not use for production or sensitive data. The encryption implementation is for demonstration purposes only.

**Current Limitations:**
- Demo encryption algorithm (not production-grade Shutter encryption)
- Testnet deployment (Chiado testnet only)
- No data persistence guarantees
- API may change without notice

## Live Deployment

**Server URL**: https://shutter-mcp-b76e270d48c5.herokuapp.com/
**Health Check**: https://shutter-mcp-b76e270d48c5.herokuapp.com/health
**MCP Endpoint**: https://shutter-mcp-b76e270d48c5.herokuapp.com/mcp

## Quick Start

### Claude Web Integration

1. Open Claude Web Settings
   - Visit [claude.ai/settings](https://claude.ai/settings)
   - Navigate to "Integrations" section

2. Add Custom Integration
   - Click "Add custom integration"
   - Enter URL: `https://shutter-mcp-b76e270d48c5.herokuapp.com/mcp`
   - Click "Add"

3. Test the Integration
   - Start a new conversation
   - Try: "Encrypt this message to unlock in 3 months: Hello future!"
   - Or: "Explain how timelock encryption works"

### VS Code MCP Integration

1. Install MCP Extension
   - Open VS Code
   - Install the "Model Context Protocol" extension
   - Or install from marketplace: `ms-vscode.vscode-mcp`

2. Configure MCP Server
   - Open VS Code settings (Ctrl+,)
   - Search for "MCP"
   - Add server configuration:
     ```json
     {
       "mcp.servers": {
         "shutter-timelock": {
           "url": "https://shutter-mcp-b76e270d48c5.herokuapp.com/mcp",
           "name": "Shutter Timelock Encryption"
         }
       }
     }
     ```

3. Test the Integration
   - Open command palette (Ctrl+Shift+P)
   - Type "MCP: Call Tool"
   - Select "timelock_encrypt" and provide parameters

## Local Development Setup

If you want to run the server locally for development:

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd shutter-mcp-server
   ```

2. **Run the deployment script**
   ```bash
   ./scripts/deploy.sh
   ```

3. **Start the server**
   ```bash
   ./scripts/start.sh
   ```

The server will be available at `http://localhost:5002` with the MCP endpoint at `http://localhost:5002/mcp`.

### Local Integration Setup

For local development, update your configurations to use:
- Claude Web: `http://localhost:5002/mcp`
- VS Code: `http://localhost:5002/mcp`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t shutter-mcp-server .
docker run -p 5002:5002 shutter-mcp-server
```

## Testing Examples

**Claude Web Test Commands:**
```
Encrypt this message to unlock in 1 hour: Secret meeting at 3pm
Check decryption status for identity: 0x1234...
Explain how timelock encryption works
```

**VS Code Test Commands:**
- Use MCP tools through the command palette
- Test timelock encryption with future timestamps
- Verify health endpoint responses

## Available Tools

### timelock_encrypt(message, unlock_time)
Encrypt a message with timelock encryption using Shutter Network.

**Parameters:**
- `message` (string): The text message to encrypt
- `unlock_time` (string): When the message can be decrypted
  - Natural language: "3 months from now", "1 year from now"
  - Unix timestamp: "1721905313"
  - Absolute date: "2024-12-25", "January 15, 2025"

**Example:**
```
timelock_encrypt("Secret auction bid: $50,000", "2024-12-31 23:59:59")
```

### check_decryption_status(identity)
Check if a timelock encrypted message is ready for decryption.

**Parameters:**
- `identity` (string): The identity returned from `timelock_encrypt`

### decrypt_timelock_message(identity, encrypted_data)
Decrypt a timelock encrypted message if the timelock has expired.

**Parameters:**
- `identity` (string): The identity returned from `timelock_encrypt`
- `encrypted_data` (string): The encrypted data returned from `timelock_encrypt`

### get_unix_timestamp(time_expression)
Convert time expressions to Unix timestamps.

**Parameters:**
- `time_expression` (string): Time to convert (default: "now")

### explain_timelock_encryption()
Get comprehensive explanation of timelock encryption and usage.

## How Timelock Encryption Works

Timelock encryption allows you to encrypt a message that can only be decrypted after a specific time. The Shutter Network uses:

- Threshold Cryptography: Distributed key generation and management
- Decentralized Keypers: Network of nodes that collectively manage decryption keys
- Time-based Release: Keys are only released after the specified timestamp
- Trustless Operation: No single party can decrypt messages early

## Use Cases

- Sealed Bid Auctions: Hide bids until auction ends
- Time-delayed Announcements: Schedule future reveals
- Dead Man's Switch: Messages that unlock if you don't check in
- Contest Reveals: Hide answers until contest ends
- Future Communications: Send messages to your future self

## Configuration

### Environment Variables

- `PORT`: Server port (default: 5002)
- `SHUTTER_API_BASE`: Shutter API endpoint (default: Chiado testnet)
- `SHUTTER_REGISTRY_ADDRESS`: Registry contract address

### Custom Configuration

Edit `src/server.py` to modify:
- API endpoints
- Timeout values
- Error handling behavior
- Additional tools

## Testing

Run the example script to test functionality:

```bash
python examples/usage_example.py
```

Health check endpoint:
```bash
curl https://shutter-mcp-b76e270d48c5.herokuapp.com/health
```

Local testing:
```bash
curl http://localhost:5002/health
```

## Project Structure

```
shutter-mcp-server/
├── src/
│   └── server.py              # Main server implementation
├── scripts/
│   ├── deploy.sh              # Deployment script
│   └── start.sh               # Start script
├── examples/
│   └── usage_example.py       # Usage examples
├── docs/
│   └── API.md                 # API documentation
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── Procfile                   # Heroku process configuration
├── deploy-heroku.ps1          # PowerShell deployment script
└── README.md                  # This file
```

## Security Considerations

**IMPORTANT: This is alpha software with significant limitations:**

- **Demo Implementation**: Current encryption is for demonstration purposes only
- **Testnet Only**: Uses Chiado testnet - not suitable for production data
- **No Production Encryption**: Does not implement full Shutter encryption algorithms yet
- **Experimental Status**: API and functionality may change without notice
- **No Data Guarantees**: No persistence or availability guarantees

**For Production Use:**
- Implement proper Shutter encryption algorithms
- Use mainnet deployment when available
- Add authentication and access controls
- Implement proper key management
- Use HTTPS in production deployments

## Troubleshooting

### Server Won't Start
- Check Python version (3.11+ required)
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check port availability: `lsof -i :5002` (Linux/Mac) or `netstat -an | findstr :5002` (Windows)

### Claude Integration Issues
- Ensure server is accessible from the internet
- Verify MCP endpoint returns proper responses: `curl https://shutter-mcp-b76e270d48c5.herokuapp.com/mcp`
- Check CORS configuration for cross-origin requests

### VS Code Integration Issues
- Verify MCP extension is installed and enabled
- Check server configuration in VS Code settings
- Use local server for development: `http://localhost:5002/mcp`

### Shutter API Errors
- Verify internet connectivity
- Check Shutter Network status
- Ensure timestamps are in the future

## Development

### Adding New Tools

1. Define the tool function with `@mcp.tool()` decorator
2. Add comprehensive docstring with parameter descriptions
3. Include proper error handling and user guidance
4. Test with the example script

### Modifying Time Parsing

Edit the `parse_time_expression` method in the `ShutterTimelock` class to support additional time formats.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Shutter Network](https://shutter.network/) for timelock encryption infrastructure
- [Model Context Protocol](https://modelcontextprotocol.io/) for the integration framework
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## Support

- Issues: Open a GitHub issue
- Documentation: See `docs/` directory
- Examples: Check `examples/` directory

---

**Version**: 2.1.0  
**Last Updated**: August 2025  
**Compatibility**: Claude Web, VS Code MCP, MCP Protocol 2024-11-05

