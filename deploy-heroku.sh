#!/bin/bash

# Heroku Deployment Script for Shutter MCP Server
# This script guides you through deploying the Shutter Timelock Encryption MCP Server to Heroku

echo "🚀 Shutter MCP Server - Heroku Deployment Script"
echo "================================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed."
    echo "Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✅ Heroku CLI found"

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please log in to Heroku:"
    heroku auth:login
fi

echo "✅ Logged in to Heroku as: $(heroku auth:whoami)"

# Create Heroku app (user will be prompted for app name)
echo ""
echo "🏗️ Creating Heroku application..."
echo "Note: App name must be unique across all Heroku apps"
read -p "Enter your desired app name (or press Enter for random name): " APP_NAME

if [ -z "$APP_NAME" ]; then
    heroku create
else
    heroku create "$APP_NAME"
fi

# Get the app URL
APP_URL=$(heroku info --json | jq -r '.app.web_url')
if [ -z "$APP_URL" ]; then
    APP_URL=$(heroku apps:info --json | jq -r '.app.web_url')
fi

echo ""
echo "✅ Heroku app created successfully!"
echo "🌐 Your app URL will be: $APP_URL"

# Deploy the application
echo ""
echo "📦 Deploying application to Heroku..."
git add .
git commit -m "Deploy Shutter MCP Server to Heroku" || echo "No changes to commit"
git push heroku main || git push heroku master

# Scale the web dyno
echo ""
echo "⚡ Scaling web dyno..."
heroku ps:scale web=1

# Show app info
echo ""
echo "📊 Application deployed successfully!"
echo "🌐 App URL: ${APP_URL}"
echo "🔗 SSE Endpoint for Claude: ${APP_URL}sse"
echo "💚 Health Check: ${APP_URL}health"

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Test your deployment: curl ${APP_URL}health"
echo "2. Add to Claude Web:"
echo "   - Go to claude.ai/settings"
echo "   - Navigate to 'Integrations'"
echo "   - Add custom integration with URL: ${APP_URL}sse"
echo "3. Start using timelock encryption in Claude!"

echo ""
echo "🔧 Useful Heroku commands:"
echo "  heroku logs --tail                # View live logs"
echo "  heroku ps                         # Check dyno status"
echo "  heroku restart                    # Restart the app"
echo "  heroku apps:destroy --confirm APP_NAME  # Delete the app"
