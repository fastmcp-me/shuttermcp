#!/usr/bin/env python3
"""
Example usage of the Shutter Timelock Encryption MCP Server

This script demonstrates how to interact with the server programmatically
for testing and development purposes.
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Server configuration
SERVER_URL = "http://localhost:5002"
HEADERS = {"Content-Type": "application/json"}

def test_server_health():
    """Test if the server is running and healthy."""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        response.raise_for_status()
        print("✅ Server is healthy:", response.json())
        return True
    except Exception as e:
        print("❌ Server health check failed:", e)
        return False

def example_timelock_encryption():
    """Example of timelock encryption workflow."""
    print("\n🔐 Timelock Encryption Example")
    print("=" * 50)
    
    # Example 1: Natural language time
    message1 = "This message will unlock in 5 minutes!"
    unlock_time1 = "5 minutes from now"
    
    print(f"Message: {message1}")
    print(f"Unlock time: {unlock_time1}")
    
    # Example 2: Unix timestamp
    future_timestamp = int((datetime.now() + timedelta(hours=1)).timestamp())
    message2 = "This message will unlock in 1 hour!"
    unlock_time2 = str(future_timestamp)
    
    print(f"\nMessage: {message2}")
    print(f"Unlock time: {unlock_time2} ({datetime.fromtimestamp(future_timestamp)})")
    
    # Example 3: Absolute date
    message3 = "Happy New Year 2025!"
    unlock_time3 = "2025-01-01"
    
    print(f"\nMessage: {message3}")
    print(f"Unlock time: {unlock_time3}")
    
    print("\nNote: This is a demonstration of the API structure.")
    print("To actually encrypt messages, you would need to integrate with the MCP protocol.")

def example_api_structure():
    """Show the expected API structure for MCP tools."""
    print("\n🛠️ MCP Tool Structure Examples")
    print("=" * 50)
    
    # Example tool calls that would be made through MCP
    examples = [
        {
            "tool": "timelock_encrypt",
            "args": {
                "message": "Secret auction bid: $50,000",
                "unlock_time": "2024-12-31 23:59:59"
            }
        },
        {
            "tool": "get_unix_timestamp",
            "args": {
                "time_expression": "3 months from now"
            }
        },
        {
            "tool": "check_decryption_status",
            "args": {
                "identity": "0x1234567890abcdef..."
            }
        },
        {
            "tool": "explain_timelock_encryption",
            "args": {}
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}: {example['tool']}")
        print(f"Arguments: {json.dumps(example['args'], indent=2)}")

if __name__ == "__main__":
    print("🚀 Shutter Timelock Encryption MCP Server - Example Usage")
    print("=" * 60)
    
    # Test server health
    if not test_server_health():
        print("\n❌ Server is not running. Please start it first:")
        print("   ./scripts/start.sh")
        exit(1)
    
    # Show examples
    example_timelock_encryption()
    example_api_structure()
    
    print("\n" + "=" * 60)
    print("📚 For full integration with Claude web:")
    print(f"   Use SSE endpoint: {SERVER_URL}/sse")
    print("   Add this URL to Claude web integrations")
    print("\n🔗 Documentation: See docs/README.md for more details")

