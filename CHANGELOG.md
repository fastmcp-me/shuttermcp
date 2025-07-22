# Changelog

All notable changes to the Shutter Timelock Encryption MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-06-25

### Added
- Complete rewrite with proper MCP protocol implementation
- SSE (Server-Sent Events) transport for Claude web integration
- Comprehensive timelock encryption using Shutter Network
- Natural language time parsing ("3 months from now")
- Unix timestamp support for precise timing
- Proper error handling and user guidance
- Docker support with health checks
- Comprehensive documentation and examples
- Production-ready deployment scripts
- API documentation with detailed examples

### Changed
- Migrated from basic HTTP to SSE protocol for MCP compatibility
- Improved Shutter API response parsing
- Enhanced error messages with helpful guidance
- Restructured project for better maintainability

### Fixed
- Shutter API response parsing issues
- Identity extraction from nested response structure
- SSE endpoint compatibility with Claude web
- CORS configuration for cross-origin requests

### Security
- Added proper error handling for API failures
- Implemented timeout handling for external API calls
- Added input validation for time expressions

## [1.0.0] - 2025-06-07

### Added
- Initial implementation of MCP server
- Basic timelock encryption functionality
- Simple HTTP-based MCP transport
- Basic Shutter Network integration

### Known Issues
- SSE protocol not properly implemented
- Response parsing issues with Shutter API
- Limited error handling and user guidance

---

## Upgrade Guide

### From 1.x to 2.0

1. **Update Dependencies**: New requirements.txt with updated MCP libraries
2. **Configuration Changes**: New environment variables and configuration options
3. **API Changes**: Tool signatures remain the same, but responses are more detailed
4. **Deployment**: New deployment scripts and Docker support available

### Breaking Changes

- SSE endpoint URL changed from `/messages` to `/sse`
- Response format enhanced with more detailed error messages
- Docker configuration updated for production use

### Migration Steps

1. Stop the old server
2. Update code to version 2.0
3. Run `./scripts/deploy.sh` to set up new environment
4. Update Claude web integration URL to use `/sse` endpoint
5. Start new server with `./scripts/start.sh`

