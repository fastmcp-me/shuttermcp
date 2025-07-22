#!/usr/bin/env python3
"""
Test suite for Shutter Timelock Encryption MCP Server

Run with: python -m pytest tests/
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import ShutterTimelock, mcp

class TestShutterTimelock:
    """Test the ShutterTimelock class functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.timelock = ShutterTimelock()
    
    def test_parse_unix_timestamp(self):
        """Test parsing of Unix timestamps."""
        # Valid future timestamp
        future_timestamp = int((datetime.now() + timedelta(days=30)).timestamp())
        result = self.timelock.parse_time_expression(str(future_timestamp))
        assert result == future_timestamp
        
        # Invalid past timestamp
        with pytest.raises(ValueError):
            self.timelock.parse_time_expression("1000000000")  # Year 2001
    
    def test_parse_natural_language(self):
        """Test parsing of natural language time expressions."""
        now = datetime.now()
        
        # Test various time expressions
        test_cases = [
            ("5 minutes from now", timedelta(minutes=5)),
            ("2 hours from now", timedelta(hours=2)),
            ("3 days from now", timedelta(days=3)),
            ("1 week from now", timedelta(weeks=1)),
        ]
        
        for expr, expected_delta in test_cases:
            result = self.timelock.parse_time_expression(expr)
            expected = int((now + expected_delta).timestamp())
            # Allow 60 second tolerance for test execution time
            assert abs(result - expected) < 60
    
    def test_parse_absolute_dates(self):
        """Test parsing of absolute date expressions."""
        # Test ISO date
        result = self.timelock.parse_time_expression("2025-12-25")
        expected = datetime(2025, 12, 25).timestamp()
        assert abs(result - expected) < 86400  # Within 1 day (timezone tolerance)
    
    def test_invalid_time_expression(self):
        """Test handling of invalid time expressions."""
        with pytest.raises(ValueError):
            self.timelock.parse_time_expression("invalid time")
    
    def test_generate_identity_prefix(self):
        """Test identity prefix generation."""
        message = "test message"
        timestamp = 1721905313
        
        prefix1 = self.timelock.generate_identity_prefix(message, timestamp)
        prefix2 = self.timelock.generate_identity_prefix(message, timestamp)
        
        # Should be different due to random component
        assert prefix1 != prefix2
        assert prefix1.startswith("0x")
        assert len(prefix1) == 66  # 0x + 64 hex chars

class TestMCPTools:
    """Test MCP tool functions."""
    
    @pytest.mark.asyncio
    async def test_get_current_time(self):
        """Test get_current_time tool."""
        # Mock the tool call
        result = await mcp._mcp_server._tools["get_current_time"].func()
        
        # Should return a string with UTC timestamp
        assert isinstance(result, str)
        assert "UTC" in result
        
        # Should be parseable as datetime
        datetime.strptime(result, "%Y-%m-%d %H:%M:%S UTC")
    
    @pytest.mark.asyncio
    async def test_get_unix_timestamp(self):
        """Test get_unix_timestamp tool."""
        # Test with "now"
        result = await mcp._mcp_server._tools["get_unix_timestamp"].func("now")
        data = json.loads(result)
        
        assert "unix_timestamp" in data
        assert "human_readable" in data
        assert isinstance(data["unix_timestamp"], int)
    
    @pytest.mark.asyncio
    async def test_explain_timelock_encryption(self):
        """Test explain_timelock_encryption tool."""
        result = await mcp._mcp_server._tools["explain_timelock_encryption"].func()
        data = json.loads(result)
        
        expected_keys = [
            "what_is_timelock_encryption",
            "how_shutter_works",
            "use_cases",
            "how_to_use",
            "example_usage"
        ]
        
        for key in expected_keys:
            assert key in data
            assert isinstance(data[key], list)
            assert len(data[key]) > 0

class TestIntegration:
    """Integration tests for the full server."""
    
    @patch('requests.post')
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_timelock_encrypt_flow(self, mock_get, mock_post):
        """Test the complete timelock encryption flow."""
        # Mock Shutter API responses
        mock_post.return_value.json.return_value = {
            "message": {
                "identity": "0x1234567890abcdef",
                "tx_hash": "0xabcdef1234567890",
                "eon_key": "0xdeadbeef"
            }
        }
        mock_post.return_value.raise_for_status.return_value = None
        
        mock_get.return_value.json.return_value = {
            "message": {
                "eon_key": "0xdeadbeef"
            }
        }
        mock_get.return_value.raise_for_status.return_value = None
        
        # Test timelock_encrypt tool
        result = await mcp._mcp_server._tools["timelock_encrypt"].func(
            "test message", "1 hour from now"
        )
        
        data = json.loads(result)
        assert data["status"] == "success"
        assert "encrypted_data" in data
        assert "identity" in data
        assert "instructions" in data

if __name__ == "__main__":
    pytest.main([__file__])

