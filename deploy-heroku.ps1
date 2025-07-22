# PowerShell Heroku Deployment Script for Shutter MCP Server
# This script guides you through deploying the Shutter Timelock Encryption MCP Server to Heroku

Write-Host "🚀 Shutter MCP Server - Heroku Deployment Script" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if Heroku CLI is installed
try {
    $null = Get-Command heroku -ErrorAction Stop
    Write-Host "✅ Heroku CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Heroku CLI is not installed." -ForegroundColor Red
    Write-Host "Please install it from: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in to Heroku
try {
    $whoami = heroku auth:whoami 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "🔐 Please log in to Heroku:" -ForegroundColor Yellow
        heroku auth:login
        $whoami = heroku auth:whoami
    }
    Write-Host "✅ Logged in to Heroku as: $whoami" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to authenticate with Heroku" -ForegroundColor Red
    exit 1
}

# Create Heroku app
Write-Host ""
Write-Host "🏗️ Creating Heroku application..." -ForegroundColor Cyan
Write-Host "Note: App name must be unique across all Heroku apps" -ForegroundColor Yellow
$APP_NAME = Read-Host "Enter your desired app name (or press Enter for random name)"

if ([string]::IsNullOrWhiteSpace($APP_NAME)) {
    heroku create
} else {
    heroku create $APP_NAME
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create Heroku app. The name might already be taken." -ForegroundColor Red
    exit 1
}

# Get the app info
$appInfo = heroku apps:info --json | ConvertFrom-Json
$APP_URL = $appInfo.app.web_url

Write-Host ""
Write-Host "✅ Heroku app created successfully!" -ForegroundColor Green
Write-Host "🌐 Your app URL will be: $APP_URL" -ForegroundColor Cyan

# Initialize git if not already done
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing git repository..." -ForegroundColor Cyan
    git init
    git branch -M main
}

# Add Heroku remote if not already added
$remotes = git remote -v
if ($remotes -notmatch "heroku") {
    $appName = $appInfo.app.name
    git remote add heroku "https://git.heroku.com/$appName.git"
}

# Deploy the application
Write-Host ""
Write-Host "📦 Deploying application to Heroku..." -ForegroundColor Cyan
git add .
try {
    git commit -m "Deploy Shutter MCP Server to Heroku"
} catch {
    Write-Host "No changes to commit" -ForegroundColor Yellow
}

Write-Host "🚀 Pushing to Heroku..." -ForegroundColor Cyan
git push heroku main
if ($LASTEXITCODE -ne 0) {
    # Try master branch if main fails
    git push heroku master
}

# Scale the web dyno
Write-Host ""
Write-Host "⚡ Scaling web dyno..." -ForegroundColor Cyan
heroku ps:scale web=1

# Show app info
Write-Host ""
Write-Host "📊 Application deployed successfully!" -ForegroundColor Green
Write-Host "🌐 App URL: $APP_URL" -ForegroundColor Cyan
Write-Host "🔗 SSE Endpoint for Claude: ${APP_URL}sse" -ForegroundColor Cyan
Write-Host "💚 Health Check: ${APP_URL}health" -ForegroundColor Cyan

Write-Host ""
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Test your deployment: Invoke-WebRequest ${APP_URL}health" -ForegroundColor White
Write-Host "2. Add to Claude Web:" -ForegroundColor White
Write-Host "   - Go to claude.ai/settings" -ForegroundColor White
Write-Host "   - Navigate to 'Integrations'" -ForegroundColor White
Write-Host "   - Add custom integration with URL: ${APP_URL}sse" -ForegroundColor White
Write-Host "3. Start using timelock encryption in Claude!" -ForegroundColor White

Write-Host ""
Write-Host "🔧 Useful Heroku commands:" -ForegroundColor Yellow
Write-Host "  heroku logs --tail                # View live logs" -ForegroundColor White
Write-Host "  heroku ps                         # Check dyno status" -ForegroundColor White
Write-Host "  heroku restart                    # Restart the app" -ForegroundColor White
Write-Host "  heroku apps:destroy --confirm APP_NAME  # Delete the app" -ForegroundColor White
