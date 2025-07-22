# Shutter Timelock Encryption MCP Server - API Documentation

## Overview

This document provides detailed API documentation for the Shutter Timelock Encryption MCP Server. The server implements the Model Context Protocol (MCP) and provides timelock encryption capabilities through the Shutter Network.

## Server Information

- **Name**: Shutter Timelock Encryption Server
- **Version**: 2.0.0
- **Protocol**: MCP 2024-11-05
- **Transport**: Server-Sent Events (SSE)

## Endpoints

### Health Check
- **URL**: `GET /health`
- **Description**: Server health and status check
- **Response**:
  ```json
  {
    "status": "healthy",
    "message": "Shutter Timelock Encryption MCP Server is running",
    "version": "2.0.0",
    "timestamp": "2024-06-25T15:30:00.000Z"
  }
  ```

### SSE Endpoint
- **URL**: `GET /sse`
- **Description**: Server-Sent Events endpoint for MCP communication
- **Headers**: `Accept: text/event-stream`
- **Response**: SSE stream with MCP protocol messages

## MCP Tools

### 1. timelock_encrypt

Encrypt a message with timelock encryption using Shutter Network.

**Parameters:**
- `message` (string, required): The text message to encrypt
- `unlock_time` (string, required): When the message can be decrypted

**Supported Time Formats:**
- Natural language: "3 months from now", "1 year from now", "5 days from now"
- Unix timestamp: "1721905313"
- Absolute date: "2024-12-25", "January 15, 2025"

**Response:**
```json
{
  "status": "success",
  "encrypted_data": "SHUTTER_ENCRYPTED:eyJtZXNzYWdlIjoi...",
  "identity": "0xa46c19255c3b735f2517483186c4a7c9e721bb28...",
  "unlock_timestamp": 1721905313,
  "unlock_date": "2024-07-25 12:15:13 UTC",
  "tx_hash": "0xaf67fd2ac9369f085f7854409456696941fb123109...",
  "instructions": {
    "how_to_decrypt": [
      "Your message will be decryptable after 2024-07-25 12:15:13 UTC",
      "Save the 'identity' value above - you'll need it to decrypt",
      "Use the 'check_decryption_status' tool to see if decryption is available",
      "Use the 'decrypt_timelock_message' tool when ready to decrypt"
    ],
    "important_info": [
      "This uses Shutter Network's timelock encryption on Chiado testnet",
      "The message cannot be decrypted before the specified time",
      "Keep the identity safe - it's needed for decryption"
    ]
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "error": "Could not parse time expression: invalid_time",
  "help": "Try using formats like '3 months from now', '1 year from now', or '2024-12-25'"
}
```

### 2. check_decryption_status

Check if a timelock encrypted message is ready for decryption.

**Parameters:**
- `identity` (string, required): The identity returned from timelock_encrypt

**Response (Ready):**
```json
{
  "status": "ready",
  "message": "Timelock has expired - message can be decrypted",
  "identity": "0xa46c19255c3b735f2517483186c4a7c9e721bb28...",
  "decryption_available": true,
  "next_step": "Use the 'decrypt_timelock_message' tool to decrypt your message"
}
```

**Response (Locked):**
```json
{
  "status": "locked",
  "message": "Timelock has not yet expired - message cannot be decrypted",
  "identity": "0xa46c19255c3b735f2517483186c4a7c9e721bb28...",
  "decryption_available": false,
  "next_step": "Wait until the unlock time has passed, then check again"
}
```

### 3. decrypt_timelock_message

Decrypt a timelock encrypted message if the timelock has expired.

**Parameters:**
- `identity` (string, required): The identity returned from timelock_encrypt
- `encrypted_data` (string, required): The encrypted data returned from timelock_encrypt

**Response (Success):**
```json
{
  "status": "success",
  "decrypted_message": "Your original message here",
  "identity": "0xa46c19255c3b735f2517483186c4a7c9e721bb28...",
  "note": "Message successfully decrypted using Shutter timelock"
}
```

**Response (Still Locked):**
```json
{
  "status": "locked",
  "message": "Timelock has not yet expired - cannot decrypt message",
  "identity": "0xa46c19255c3b735f2517483186c4a7c9e721bb28..."
}
```

### 4. get_unix_timestamp

Convert time expressions to Unix timestamps.

**Parameters:**
- `time_expression` (string, optional): Time to convert (default: "now")

**Response:**
```json
{
  "unix_timestamp": 1721905313,
  "human_readable": "2024-07-25 12:15:13 UTC",
  "time_expression": "3 months from now",
  "note": "Use the unix_timestamp value for precise timelock encryption"
}
```

### 5. get_current_time

Get the current date and time in UTC.

**Parameters:** None

**Response:**
```
"2024-06-25 15:30:00 UTC"
```

### 6. explain_timelock_encryption

Get comprehensive explanation of timelock encryption and usage.

**Parameters:** None

**Response:**
```json
{
  "what_is_timelock_encryption": [
    "Timelock encryption allows you to encrypt a message that can only be decrypted after a specific time",
    "The message is cryptographically locked until the specified timestamp",
    "Even if someone has the encrypted data, they cannot decrypt it before the unlock time"
  ],
  "how_shutter_works": [
    "Shutter Network uses threshold cryptography and a decentralized network of keypers",
    "When you encrypt a message, you specify a future timestamp",
    "The keypers will only release the decryption key after that timestamp",
    "This provides trustless timelock encryption without relying on a single party"
  ],
  "use_cases": [
    "Time-delayed messages and announcements",
    "Sealed bid auctions",
    "Scheduled reveals for games or contests",
    "Future-dated communications",
    "Dead man's switch scenarios"
  ],
  "how_to_use": [
    "1. Use 'timelock_encrypt' with your message and unlock time",
    "2. Save the returned identity and encrypted data",
    "3. Use 'check_decryption_status' to see if unlock time has passed",
    "4. Use 'decrypt_timelock_message' to decrypt when ready"
  ],
  "example_usage": [
    "timelock_encrypt('Happy New Year!', '2025-01-01')",
    "timelock_encrypt('Secret birthday message', '3 months from now')",
    "timelock_encrypt('Auction results', '1782360000')"
  ]
}
```

## Error Handling

All tools return structured error responses when issues occur:

```json
{
  "status": "error",
  "error": "Detailed error message",
  "help": "Guidance on how to fix the issue"
}
```

Common error scenarios:
- Invalid time expressions
- Network connectivity issues
- Shutter API errors
- Invalid parameters

## Time Expression Parsing

The server supports flexible time expression parsing:

### Natural Language
- "5 minutes from now"
- "3 hours from now"
- "2 days from now"
- "1 week from now"
- "6 months from now"
- "2 years from now"

### Absolute Dates
- "2024-12-25"
- "January 15, 2025"
- "2025-01-01 12:00:00"

### Unix Timestamps
- "1721905313" (numeric string)
- Must be in the future (after 2024)

## Integration Examples

### Claude Web Integration

1. Add the SSE endpoint to Claude web integrations:
   ```
   https://your-server.com:5002/sse
   ```

2. Use natural language in Claude:
   ```
   "Encrypt this message to unlock in 3 months: Happy anniversary!"
   ```

### Programmatic Usage

```python
# Example MCP tool call structure
{
  "method": "tools/call",
  "params": {
    "name": "timelock_encrypt",
    "arguments": {
      "message": "Secret auction bid: $50,000",
      "unlock_time": "2024-12-31 23:59:59"
    }
  }
}
```

## Rate Limits and Constraints

- **Shutter API**: Subject to Shutter Network rate limits
- **Time Range**: Minimum 1 minute in the future
- **Message Size**: No explicit limit, but reasonable sizes recommended
- **Concurrent Requests**: Limited by server resources

## Security Considerations

- **Demo Encryption**: Current implementation uses demo encryption
- **Production Use**: Implement proper Shutter encryption algorithms
- **Identity Storage**: Store identities securely for future decryption
- **Network Security**: Use HTTPS in production

## Monitoring and Debugging

### Health Check
```bash
curl http://localhost:5002/health
```

### SSE Connection Test
```bash
curl -H "Accept: text/event-stream" http://localhost:5002/sse
```

### Log Levels
- INFO: Normal operations
- ERROR: Error conditions
- DEBUG: Detailed debugging (set log level in uvicorn)

---

**API Version**: 2.0.0  
**Last Updated**: June 2025  
**Protocol Compatibility**: MCP 2024-11-05

