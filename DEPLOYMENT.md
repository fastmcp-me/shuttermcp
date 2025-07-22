# 🚀 Quick Heroku Deployment Guide

Your Shutter MCP Server has been successfully deployed to Heroku!

## 🌐 Your Live Server URLs

- **Main Server**: https://shutter-mcp-timelock-9db5ad982744.herokuapp.com/
- **Health Check**: https://shutter-mcp-timelock-9db5ad982744.herokuapp.com/health
- **SSE Endpoint for Claude**: https://shutter-mcp-timelock-9db5ad982744.herokuapp.com/sse

## 🔗 Adding to Claude Web

1. **Go to Claude Web Settings**
   - Visit [claude.ai/settings](https://claude.ai/settings)
   - Navigate to "Integrations" section

2. **Add Custom Integration**
   - Click "Add custom integration"
   - Enter URL: `https://shutter-mcp-timelock-9db5ad982744.herokuapp.com/sse`
   - Click "Add"

3. **Test the Integration**
   - Start a new conversation
   - Try: "Encrypt this message to unlock in 3 months: Hello future!"
   - Or: "Explain how timelock encryption works"

## 🧪 Testing Your Deployment

Test with PowerShell:
```powershell
# Health check
Invoke-WebRequest -Uri "https://shutter-mcp-timelock-9db5ad982744.herokuapp.com/health"

# Server info
Invoke-WebRequest -Uri "https://shutter-mcp-timelock-9db5ad982744.herokuapp.com/"
```

## 🔧 Managing Your Heroku App

```bash
# View logs
heroku logs --tail

# Check dyno status
heroku ps

# Restart the app
heroku restart

# Scale up/down
heroku ps:scale web=1

# Open app in browser
heroku open

# Delete the app (if needed)
heroku apps:destroy --confirm shutter-mcp-timelock
```

## 📊 Monitoring

- **Heroku Dashboard**: https://dashboard.heroku.com/apps/shutter-mcp-timelock
- **App Logs**: `heroku logs --tail`
- **Health Endpoint**: https://shutter-mcp-timelock-9db5ad982744.herokuapp.com/health

## 🎉 Success!

Your Shutter Timelock Encryption MCP Server is now live and ready to use with Claude Web!

---

**App Name**: shutter-mcp-timelock  
**Deployment Date**: July 22, 2025  
**Status**: ✅ Active and Running
