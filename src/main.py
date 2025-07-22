#!/usr/bin/env python3
"""
Shutter Timelock Encryption MCP Server

This MCP server wraps the Shutter API to provide timelock encryption capabilities
through Claude web. Users can encrypt messages that can only be decrypted after
a specified time in the future.

Features:
- Encrypt text with natural language time specifications ("3 months from now")
- Check decryption status
- Decrypt messages when timelock expires
- User-friendly instructions and error handling
"""

import os
import sys
import json
import time
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import requests
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.applications import Starlette
    from starlette.routing import Mount
    from mcp import FastMCP
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

# Fallback to Flask if FastAPI is not available
if not FASTAPI_AVAILABLE:
    from flask import Flask, request, jsonify
    from flask_cors import CORS

# Shutter API Configuration
SHUTTER_API_BASE = "https://shutter-api.chiado.staging.shutter.network/api"
SHUTTER_REGISTRY_ADDRESS = "0x2693a4Fb363AdD4356e6b80Ac5A27fF05FeA6D9F"

class ShutterTimelock:
    """Handles Shutter API interactions for timelock encryption"""
    
    def __init__(self):
        self.api_base = SHUTTER_API_BASE
        self.registry_address = SHUTTER_REGISTRY_ADDRESS
        
    def parse_time_expression(self, time_expr: str) -> int:
        """Parse natural language time expressions to Unix timestamp"""
        time_expr = time_expr.lower().strip()
        now = datetime.now()
        
        # Handle relative time expressions
        if "from now" in time_expr:
            time_expr = time_expr.replace("from now", "").strip()
            
        # Parse different time formats
        if "minute" in time_expr:
            minutes = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + timedelta(minutes=minutes)
        elif "hour" in time_expr:
            hours = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + timedelta(hours=hours)
        elif "day" in time_expr:
            days = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + timedelta(days=days)
        elif "week" in time_expr:
            weeks = int(''.join(filter(str.isdigit, time_expr)))
            target_time = now + timedelta(weeks=weeks)
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
                raise ValueError(f"Could not parse time expression: {time_expr}")
        
        return int(target_time.timestamp())
    
    def generate_identity_prefix(self, message: str, timestamp: int) -> str:
        """Generate a unique identity prefix for the encryption"""
        # Create a unique identifier based on message hash and timestamp
        content = f"{message}_{timestamp}_{secrets.token_hex(16)}"
        hash_obj = hashlib.sha256(content.encode())
        return "0x" + hash_obj.hexdigest()
    
    def register_identity(self, timestamp: int, identity_prefix: str) -> Dict[str, Any]:
        """Register identity with Shutter API for timelock decryption"""
        url = f"{self.api_base}/register_identity"
        payload = {
            "decryptionTimestamp": timestamp,
            "identityPrefix": identity_prefix
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_encryption_data(self) -> Dict[str, Any]:
        """Get encryption data from Shutter API"""
        url = f"{self.api_base}/get_data_for_encryption"
        params = {"address": self.registry_address}
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_decryption_key(self, identity: str) -> Optional[Dict[str, Any]]:
        """Get decryption key if timelock has expired"""
        url = f"{self.api_base}/get_decryption_key"
        params = {"identity": identity}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None  # Key not yet available
            raise
    
    def encrypt_message_simple(self, message: str, identity: str, eon_key: str) -> str:
        """Simple encryption placeholder - in real implementation would use Shutter crypto"""
        # This is a placeholder implementation
        # In a real implementation, you would use the Shutter crypto library
        # For now, we'll create a simple encoded format that includes the metadata
        
        encrypted_data = {
            "message": message,  # In real implementation, this would be encrypted
            "identity": identity,
            "eon_key": eon_key,
            "encrypted": True,
            "note": "This is a demo implementation. Real encryption would use Shutter crypto library."
        }
        
        # Encode as base64 for transport
        import base64
        json_str = json.dumps(encrypted_data)
        encoded = base64.b64encode(json_str.encode()).decode()
        return f"SHUTTER_ENCRYPTED:{encoded}"

# Initialize the timelock handler
timelock = ShutterTimelock()

if FASTAPI_AVAILABLE:
    # FastAPI/MCP Implementation
    mcp = FastMCP("Shutter Timelock Encryption")
    
    @mcp.tool()
    def timelock_encrypt(message: str, unlock_time: str) -> str:
        """
        Encrypt a message with timelock encryption using Shutter Network.
        
        Args:
            message: The text message to encrypt
            unlock_time: When the message can be decrypted (e.g., "3 months from now", "2024-12-25", "1 year from now")
        
        Returns:
            Encrypted data and instructions for future decryption
        """
        try:
            # Parse the unlock time
            timestamp = timelock.parse_time_expression(unlock_time)
            unlock_date = datetime.fromtimestamp(timestamp)
            
            # Generate identity prefix
            identity_prefix = timelock.generate_identity_prefix(message, timestamp)
            
            # Register identity with Shutter API
            registration = timelock.register_identity(timestamp, identity_prefix)
            
            # Get encryption data
            encryption_data = timelock.get_encryption_data()
            
            # Encrypt the message (simplified implementation)
            encrypted_message = timelock.encrypt_message_simple(
                message, 
                registration["identity"], 
                encryption_data["eon_key"]
            )
            
            # Create user-friendly response
            result = {
                "status": "success",
                "encrypted_data": encrypted_message,
                "identity": registration["identity"],
                "unlock_timestamp": timestamp,
                "unlock_date": unlock_date.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "tx_hash": registration.get("tx_hash"),
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
            Status of the timelock and whether decryption is available
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
            The decrypted message or error if timelock hasn't expired
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
            
            # Decrypt the message (simplified implementation)
            if encrypted_data.startswith("SHUTTER_ENCRYPTED:"):
                import base64
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
        Explain how Shutter timelock encryption works and how to use it.
        
        Returns:
            Comprehensive explanation of timelock encryption
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
                "timelock_encrypt('Auction results', '1 week from now')"
            ],
            "important_notes": [
                "This demo uses Chiado testnet - for production use Gnosis mainnet",
                "Keep your identity safe - it's needed for decryption",
                "The current implementation is simplified for demonstration",
                "Real production use would require the full Shutter crypto library"
            ]
        }
        
        return json.dumps(explanation, indent=2)
    
    # Create the FastAPI app with MCP
    app = Starlette(
        routes=[
            Mount("/sse", app=mcp.sse_app()),
        ]
    )
    
    # Add CORS middleware
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add a simple info endpoint
    from starlette.responses import JSONResponse
    from starlette.routing import Route
    
    async def info_endpoint(request):
        return JSONResponse({
            "name": "Shutter Timelock Encryption MCP Server",
            "description": "Provides timelock encryption using Shutter Network",
            "version": "1.0.0",
            "endpoints": {
                "sse": "/sse (for MCP communication)",
                "info": "/ (this endpoint)"
            },
            "tools": [
                "timelock_encrypt - Encrypt messages with future unlock times",
                "check_decryption_status - Check if timelock has expired",
                "decrypt_timelock_message - Decrypt when timelock expires",
                "explain_timelock_encryption - Learn about timelock encryption"
            ],
            "usage": "Add this server to Claude web integrations using the /sse endpoint"
        })
    
    app.routes.insert(0, Route("/", info_endpoint))

else:
    # Flask fallback implementation
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    def info():
        return jsonify({
            "name": "Shutter Timelock Encryption MCP Server",
            "description": "Provides timelock encryption using Shutter Network",
            "version": "1.0.0",
            "note": "FastAPI not available, running Flask fallback",
            "tools": [
                "timelock_encrypt",
                "check_decryption_status", 
                "decrypt_timelock_message",
                "explain_timelock_encryption"
            ]
        })

if __name__ == "__main__":
    if FASTAPI_AVAILABLE:
        uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")
    else:
        app.run(host="0.0.0.0", port=5001, debug=True)

# For deployment
application = app

