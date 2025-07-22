# Shutter Timelock Encryption MCP Server

A Model Context Protocol (MCP) server that provides timelock encryption capabilities using the Shutter Network. This server allows users to encrypt messages that can only be decrypted after a specified future time, enabling trustless time-delayed communications.

## 🌟 Features

- **Timelock Encryption**: Encrypt messages that unlock at future timestamps
- **Natural Language Time Parsing**: Use expressions like "3 months from now"
- **Unix Timestamp Support**: Direct timestamp input for precise timing
- **Claude Web Integration**: SSE protocol support for seamless Claude integration
- **Comprehensive Error Handling**: User-friendly error messages and guidance
- **Production Ready**: Docker support, health checks, and monitoring

## 🚀 Quick Start

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

The server will be available at `http://localhost:5002` with the SSE endpoint at `http://localhost:5002/sse`.

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t shutter-mcp-server .
docker run -p 5002:5002 shutter-mcp-server
```

## 🔗 Claude Web Integration

1. **Go to Claude Web Settings**
   - Visit [claude.ai/settings](https://claude.ai/settings)
   - Navigate to "Integrations" section

2. **Add Custom Integration**
   - Click "Add custom integration"
   - Enter URL: `http://your-server:5002/sse`
   - Click "Add"

3. **Test the Integration**
   - Start a new conversation
   - Try: "Encrypt this message to unlock in 3 months: Hello future!"
   - Or: "Explain how timelock encryption works"

## 🛠️ Available Tools

### `timelock_encrypt(message, unlock_time)`
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

### `check_decryption_status(identity)`
Check if a timelock encrypted message is ready for decryption.

**Parameters:**
- `identity` (string): The identity returned from `timelock_encrypt`

### `decrypt_timelock_message(identity, encrypted_data)`
Decrypt a timelock encrypted message if the timelock has expired.

**Parameters:**
- `identity` (string): The identity returned from `timelock_encrypt`
- `encrypted_data` (string): The encrypted data returned from `timelock_encrypt`

### `get_unix_timestamp(time_expression)`
Convert time expressions to Unix timestamps.

**Parameters:**
- `time_expression` (string): Time to convert (default: "now")

### `explain_timelock_encryption()`
Get comprehensive explanation of timelock encryption and usage.

## 📖 How Timelock Encryption Works

Timelock encryption allows you to encrypt a message that can only be decrypted after a specific time. The Shutter Network uses:

- **Threshold Cryptography**: Distributed key generation and management
- **Decentralized Keypers**: Network of nodes that collectively manage decryption keys
- **Time-based Release**: Keys are only released after the specified timestamp
- **Trustless Operation**: No single party can decrypt messages early

## 🎯 Use Cases

- **Sealed Bid Auctions**: Hide bids until auction ends
- **Time-delayed Announcements**: Schedule future reveals
- **Dead Man's Switch**: Messages that unlock if you don't check in
- **Contest Reveals**: Hide answers until contest ends
- **Future Communications**: Send messages to your future self

## 🔧 Configuration

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

## 🧪 Testing

Run the example script to test functionality:

```bash
python examples/usage_example.py
```

Health check endpoint:
```bash
curl http://localhost:5002/health
```

## 📁 Project Structure

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
└── README.md                  # This file
```

## 🔒 Security Considerations

- **Demo Implementation**: Current encryption is for demonstration purposes
- **Production Use**: Implement proper Shutter encryption algorithms
- **Network Security**: Use HTTPS in production deployments
- **Access Control**: Consider authentication for sensitive deployments

## 🐛 Troubleshooting

### Server Won't Start
- Check Python version (3.11+ required)
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check port availability: `lsof -i :5002`

### Claude Integration Issues
- Ensure server is accessible from the internet
- Verify SSE endpoint returns proper events: `curl -H "Accept: text/event-stream" http://your-server:5002/sse`
- Check CORS configuration for cross-origin requests

### Shutter API Errors
- Verify internet connectivity
- Check Shutter Network status
- Ensure timestamps are in the future

## 📝 Development

### Adding New Tools

1. Define the tool function with `@mcp.tool()` decorator
2. Add comprehensive docstring with parameter descriptions
3. Include proper error handling and user guidance
4. Test with the example script

### Modifying Time Parsing

Edit the `parse_time_expression` method in the `ShutterTimelock` class to support additional time formats.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [Shutter Network](https://shutter.network/) for timelock encryption infrastructure
- [Model Context Protocol](https://modelcontextprotocol.io/) for the integration framework
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## 📞 Support

- **Issues**: Open a GitHub issue
- **Documentation**: See `docs/` directory
- **Examples**: Check `examples/` directory

---

**Version**: 2.0.0  
**Last Updated**: June 2025  
**Compatibility**: Claude Web, MCP Protocol 2024-11-05

