#!/bin/bash
# Deployment script for Shutter Timelock Encryption MCP Server

set -e

echo "🚀 Deploying Shutter Timelock Encryption MCP Server..."

# Check if Python 3.11+ is available
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.11+ is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Set default port if not specified
export PORT=${PORT:-5002}

echo "✅ Deployment complete!"
echo ""
echo "🌐 Server Configuration:"
echo "   Port: $PORT"
echo "   SSE Endpoint: http://localhost:$PORT/sse"
echo "   Health Check: http://localhost:$PORT/health"
echo ""
echo "🚀 To start the server, run:"
echo "   source venv/bin/activate"
echo "   python src/server.py"
echo ""
echo "🔗 For Claude web integration, use:"
echo "   http://your-domain:$PORT/sse"

