#!/bin/bash
# Start script for Shutter Timelock Encryption MCP Server

set -e

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./scripts/deploy.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set default port if not specified
export PORT=${PORT:-5002}

echo "🚀 Starting Shutter Timelock Encryption MCP Server..."
echo "   Port: $PORT"
echo "   SSE Endpoint: http://localhost:$PORT/sse"
echo "   Health Check: http://localhost:$PORT/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python src/server.py

