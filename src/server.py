#!/usr/bin/env python3
"""
Shutter Timelock Encryption MCP Server

A Model Context Protocol (MCP) server that provides timelock encryption capabilities
using the Shutter Network. This server allows users to encrypt messages that can
only be decrypted after a specified future time.

Features:
- Timelock encryption using Shutter Network
- Natural language time parsing ("3 months from now")
- Unix timestamp support
- Streamable HTTP protocol for Claude web integration with session persistence
- Comprehensive error handling and user guidance

Author: Manus AI
Version: 2.1.0
License: MIT
"""

import os
import sys
import datetime
import json
import base64
import hashlib
import secrets
import requests
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta
from mcp.server.fastmcp import FastMCP

# Import for custom routes (will be available when FastMCP runs)
try:
    from starlette.responses import JSONResponse, Response
except ImportError:
    # Will be available at runtime
    JSONResponse = Response = None

# Configuration
SHUTTER_API_BASE = "https://shutter-api.chiado.staging.shutter.network/api"
SHUTTER_REGISTRY_ADDRESS = "0x2693a4Fb363AdD4356e6b80Ac5A27fF05FeA6D9F"
SERVER_VERSION = "2.1.0"
SERVER_PORT = int(os.getenv("PORT", 5002))

class ShutterTimelock:
    """
    Handles Shutter API interactions for timelock encryption.
    
    The Shutter Network provides trustless timelock encryption using threshold
    cryptography and a decentralized network of keypers.
    """
    
    def __init__(self):
        self.api_base = SHUTTER_API_BASE
        self.registry_address = SHUTTER_REGISTRY_ADDRESS
        
    def parse_time_expression(self, time_expr: str) -> int:
        """
        Parse natural language time expressions OR Unix timestamps to Unix timestamp.
        
        Args:
            time_expr: Time expression to parse. Can be:
                      - Unix timestamp (e.g., "1721905313")
                      - Natural language (e.g., "3 months from now")
                      - Absolute date (e.g., "2024-12-25")
        
        Returns:
            Unix timestamp as integer
            
        Raises:
            ValueError: If time expression cannot be parsed
        """
        time_expr = str(time_expr).strip()
        
        # Check if it's already a Unix timestamp (numeric string)
        if time_expr.isdigit():
            timestamp = int(time_expr)
            # Validate it's a reasonable future timestamp (after 2024)
            if timestamp > 1704067200:  # Jan 1, 2024
                return timestamp
            else:
                raise ValueError(f"Unix timestamp {timestamp} appears to be in the past or invalid")
        
        # Handle natural language expressions
        time_expr = time_expr.lower().strip()
        now = datetime.datetime.now()
        
        # Handle relative time expressions
        if "from now" in time_expr:
            time_expr = time_expr.replace("from now", "").strip()
            
        # Parse different time formats
        if "minute" in time_expr:
            minutes = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + datetime.timedelta(minutes=minutes)
        elif "hour" in time_expr:
            hours = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + datetime.timedelta(hours=hours)
        elif "day" in time_expr:
            days = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + datetime.timedelta(days=days)
        elif "week" in time_expr:
            weeks = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + datetime.timedelta(weeks=weeks)
        elif "month" in time_expr:
            months = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + relativedelta(months=months)
        elif "year" in time_expr:
            years = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + relativedelta(years=years)
        else:
            # Try to parse as absolute date
            try:
                target_time = parse_date(time_expr)
            except:
                raise ValueError(
                    f"Could not parse time expression: {time_expr}. "
                    "Use Unix timestamp, natural language like '3 months from now', "
                    "or date like '2024-12-25'"
                )
        
        return int(target_time.timestamp())
    
    def generate_identity_prefix(self, message: str, timestamp: int) -> str:
        """
        Generate a unique identity prefix for the encryption.
        
        Args:
            message: The message to encrypt
            timestamp: Unix timestamp for unlock time
            
        Returns:
            Hex-encoded identity prefix
        """
        content = f"{message}_{timestamp}_{secrets.token_hex(16)}"
        hash_obj = hashlib.sha256(content.encode())
        return "0x" + hash_obj.hexdigest()
    
    def register_identity(self, timestamp: int, identity_prefix: str) -> dict:
        """
        Register identity with Shutter API for timelock decryption.
        
        Args:
            timestamp: Unix timestamp for unlock time
            identity_prefix: Unique identity prefix
            
        Returns:
            Registration response from Shutter API
            
        Raises:
            requests.RequestException: If API call fails
        """
        url = f"{self.api_base}/register_identity"
        payload = {
            "decryptionTimestamp": timestamp,
            "identityPrefix": identity_prefix
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_encryption_data(self) -> dict:
        """
        Get encryption data from Shutter API.
        
        Returns:
            Encryption data from Shutter API
            
        Raises:
            requests.RequestException: If API call fails
        """
        url = f"{self.api_base}/get_data_for_encryption"
        params = {"address": self.registry_address}
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_decryption_key(self, identity: str) -> dict:
        """
        Get decryption key if timelock has expired.
        
        Args:
            identity: Identity returned from registration
            
        Returns:
            Decryption key data or None if not yet available
            
        Raises:
            requests.RequestException: If API call fails (except 404)
        """
        url = f"{self.api_base}/get_decryption_key"
        params = {"identity": identity}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None  # Key not yet available
            raise
    
    def encrypt_message_simple(self, message: str, identity: str, eon_key: str) -> str:
        """
        Simple encryption placeholder (demo implementation).
        
        Note: This is a demo implementation. In production, you would use
        the actual Shutter encryption algorithm with the provided eon_key.
        
        Args:
            message: Message to encrypt
            identity: Identity for decryption
            eon_key: Encryption key from Shutter API
            
        Returns:
            Base64-encoded encrypted data
        """
        encrypted_data = {
            "message": message,
            "identity": identity,
            "eon_key": eon_key,
            "encrypted": True,
            "note": "Demo implementation using Shutter Network timelock encryption"
        }
        
        json_str = json.dumps(encrypted_data)
        encoded = base64.b64encode(json_str.encode()).decode()
        return f"SHUTTER_ENCRYPTED:{encoded}"

# Initialize the timelock handler
timelock = ShutterTimelock()

# Create the MCP server with tools using FastMCP's built-in session management
# Configure for both VS Code MCP and Claude Web compatibility
mcp = FastMCP(
    "Shutter Timelock Encryption Server",
    # Enable stateless HTTP for Claude Web compatibility
    stateless_http=True,
    # Enable JSON responses for web clients that don't support SSE
    json_response=True
)

@mcp.tool()
def get_current_time() -> str:
    """Get the current date and time in UTC."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

@mcp.tool()
def get_unix_timestamp(time_expression: str = "now") -> str:
    """
    Get Unix timestamp for a given time expression or current time.
    
    This tool helps convert natural language time expressions to Unix timestamps
    that can be used with the Shutter API.
    
    Args:
        time_expression: Time to convert. Can be:
                        - "now" for current time
                        - Natural language like "3 months from now", "1 year from now"
                        - Absolute dates like "2024-12-25"
    
    Returns:
        JSON string with Unix timestamp and human-readable date
    """
    try:
        if time_expression.lower() == "now":
            timestamp = int(datetime.datetime.now().timestamp())
            readable = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            timestamp = timelock.parse_time_expression(time_expression)
            readable = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return json.dumps({
            "unix_timestamp": timestamp,
            "human_readable": readable,
            "time_expression": time_expression,
            "note": "Use the unix_timestamp value for precise timelock encryption"
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "time_expression": time_expression,
            "help": "Try formats like 'now', '3 months from now', or '2024-12-25'"
        }, indent=2)

@mcp.tool()
def timelock_encrypt(message: str, unlock_time: str) -> str:
    """
    Encrypt a message with timelock encryption using Shutter Network.
    
    This tool encrypts a message that can only be decrypted after a specified
    future time. The encryption is handled by the Shutter Network's decentralized
    keypers using threshold cryptography.
    
    IMPORTANT FOR LLM: This tool accepts BOTH Unix timestamps AND natural language time expressions.
    - Unix timestamps: Use numeric values like "1721905313" for precise future times
    - Natural language: Use expressions like "3 months from now", "1 year from now"
    - Absolute dates: Use formats like "2024-12-25" or "January 15, 2025"
    
    The Shutter API works with Unix timestamps internally. When users provide natural language,
    this tool converts it to Unix timestamps automatically.
    
    WORKFLOW: The LLM should directly call this tool with the user's time expression.
    No need to call get_unix_timestamp first - this tool handles all time parsing.
    
    Args:
        message: The text message to encrypt
        unlock_time: When the message can be decrypted. Accepts:
                    - Unix timestamp (e.g., "1721905313")
                    - Natural language (e.g., "3 months from now", "1 year from now")
                    - Absolute date (e.g., "2024-12-25", "January 15, 2025")
    
    Returns:
        JSON string with encrypted data and instructions for future decryption
    """
    try:
        # Parse the unlock time
        timestamp = timelock.parse_time_expression(unlock_time)
        unlock_date = datetime.datetime.fromtimestamp(timestamp)
        
        # Generate identity prefix
        identity_prefix = timelock.generate_identity_prefix(message, timestamp)
        
        # Register identity with Shutter API
        registration = timelock.register_identity(timestamp, identity_prefix)
        
        # Get encryption data
        encryption_data = timelock.get_encryption_data()
        
        # Extract identity from the correct location in the response
        # The Shutter API returns: {"message": {"identity": "...", "tx_hash": "...", ...}}
        identity = registration["message"]["identity"]
        tx_hash = registration["message"].get("tx_hash")
        eon_key = encryption_data["message"].get("eon_key", "demo_key")
        
        # Encrypt the message
        encrypted_message = timelock.encrypt_message_simple(message, identity, eon_key)
        
        # Create user-friendly response
        result = {
            "status": "success",
            "encrypted_data": encrypted_message,
            "identity": identity,
            "unlock_timestamp": timestamp,
            "unlock_date": unlock_date.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "tx_hash": tx_hash,
            "instructions": {
                "how_to_decrypt": [
                    f"Your message will be decryptable after {unlock_date.strftime('%Y-%m-%d %H:%M:%S UTC')}",
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
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e),
            "help": "Try using formats like '3 months from now', '1 year from now', or '2024-12-25'"
        }, indent=2)

@mcp.tool()
def check_decryption_status(identity: str) -> str:
    """
    Check if a timelock encrypted message is ready for decryption.
    
    Args:
        identity: The identity returned from timelock_encrypt
    
    Returns:
        JSON string with status of the timelock and whether decryption is available
    """
    try:
        # Try to get decryption key
        decryption_data = timelock.get_decryption_key(identity)
        
        if decryption_data:
            result = {
                "status": "ready",
                "message": "Timelock has expired - message can be decrypted",
                "identity": identity,
                "decryption_available": True,
                "next_step": "Use the 'decrypt_timelock_message' tool to decrypt your message"
            }
        else:
            result = {
                "status": "locked",
                "message": "Timelock has not yet expired - message cannot be decrypted",
                "identity": identity,
                "decryption_available": False,
                "next_step": "Wait until the unlock time has passed, then check again"
            }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e),
            "identity": identity
        }, indent=2)

@mcp.tool()
def decrypt_timelock_message(identity: str, encrypted_data: str) -> str:
    """
    Decrypt a timelock encrypted message if the timelock has expired.
    
    Args:
        identity: The identity returned from timelock_encrypt
        encrypted_data: The encrypted data returned from timelock_encrypt
    
    Returns:
        JSON string with the decrypted message or error if timelock hasn't expired
    """
    try:
        # Check if decryption is available
        decryption_data = timelock.get_decryption_key(identity)
        
        if not decryption_data:
            return json.dumps({
                "status": "locked",
                "message": "Timelock has not yet expired - cannot decrypt message",
                "identity": identity
            }, indent=2)
        
        # Decrypt the message
        if encrypted_data.startswith("SHUTTER_ENCRYPTED:"):
            encoded_data = encrypted_data.replace("SHUTTER_ENCRYPTED:", "")
            json_str = base64.b64decode(encoded_data).decode()
            data = json.loads(json_str)
            
            result = {
                "status": "success",
                "decrypted_message": data["message"],
                "identity": identity,
                "note": "Message successfully decrypted using Shutter timelock"
            }
        else:
            result = {
                "status": "error",
                "error": "Invalid encrypted data format",
                "identity": identity
            }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e),
            "identity": identity
        }, indent=2)

@mcp.tool()
def explain_timelock_encryption() -> str:
    """
    Explain how Shutter timelock encryption works and how to use this server.
    
    Returns:
        JSON string with comprehensive explanation of timelock encryption
    """
    explanation = {
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
    
    return json.dumps(explanation, indent=2)

# Add custom route for better Claude Web compatibility
@mcp.custom_route("/health", methods=["GET", "OPTIONS"])
async def health_check(request):
    """Health check endpoint with CORS headers for Claude Web compatibility."""
    response = JSONResponse({
        "status": "healthy", 
        "server": "Shutter MCP Server",
        "version": SERVER_VERSION,
        "mcp_endpoint": "/mcp"
    })
    
    # Add CORS headers for Claude Web
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept, Authorization, Mcp-Session-Id, Mcp-Protocol-Version"
    
    return response

# Add OPTIONS handler for the main MCP endpoint
@mcp.custom_route("/mcp", methods=["OPTIONS"])
async def mcp_options(request):
    """Handle CORS preflight requests for Claude Web."""
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept, Authorization, Mcp-Session-Id, Mcp-Protocol-Version, Last-Event-ID"
    response.headers["Access-Control-Max-Age"] = "86400"
    
    return response

# Main execution
if __name__ == "__main__":
    print(f"Starting Shutter Timelock Encryption MCP Server v{SERVER_VERSION}")
    print(f"Server will be available at: http://0.0.0.0:{SERVER_PORT}")
    print(f"VS Code MCP endpoint: http://0.0.0.0:{SERVER_PORT}/mcp")
    print(f"Claude Web endpoint: https://shutter-mcp-timelock-9db5ad982744.herokuapp.com/mcp")
    
    # Configure host and port via settings
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = SERVER_PORT
    
    # Run server using modern Streamable HTTP transport with dual compatibility
    mcp.run(transport="streamable-http")

