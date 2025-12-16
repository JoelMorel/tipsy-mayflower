# Railway Deployment Guide

This guide will help you deploy Tipsy Mayflower to Railway.

## Prerequisites

- A Railway account (sign up at [railway.app](https://railway.app))
- Your API keys ready:
  - Google Maps API Key
  - Yelp API Key
  - A Flask Secret Key (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)

## Deployment Steps

### Option 1: Deploy via GitHub (Recommended)

1. **Push your code to GitHub** (if not already done):

   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Create a new Railway project**:

   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**:

   - In your Railway project dashboard, go to "Variables"
   - Add the following environment variables:
     ```
     GOOGLE_MAPS_API_KEY=your_google_maps_api_key
     YELP_API_KEY=your_yelp_api_key
     SECRET_KEY=your_generated_secret_key
     FLASK_DEBUG=0
     ```
   - Optionally set `WEB_CONCURRENCY` (defaults to 2 workers)

4. **Deploy**:

   - Railway will automatically detect your Python app
   - It will use your `Procfile` to start the application
   - The deployment will begin automatically

5. **Get your app URL**:
   - Once deployed, Railway will provide you with a public URL
   - You can also set up a custom domain in the "Settings" tab

### Option 2: Deploy via Railway CLI

1. **Install Railway CLI**:

   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**:

   ```bash
   railway login
   ```

3. **Initialize Railway in your project**:

   ```bash
   railway init
   ```

4. **Set environment variables**:

   ```bash
   railway variables set GOOGLE_MAPS_API_KEY=your_key
   railway variables set YELP_API_KEY=your_key
   railway variables set SECRET_KEY=your_secret
   railway variables set FLASK_DEBUG=0
   ```

5. **Deploy**:
   ```bash
   railway up
   ```

## Configuration Files

Your app is already configured with:

- ✅ `Procfile` - Defines the web process
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version (3.11.9)
- ✅ `railway.json` - Railway-specific configuration

## Environment Variables

| Variable              | Description                       | Required | Default |
| --------------------- | --------------------------------- | -------- | ------- |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key               | Yes      | -       |
| `YELP_API_KEY`        | Yelp API key                      | Yes      | -       |
| `SECRET_KEY`          | Flask secret key                  | Yes      | -       |
| `FLASK_DEBUG`         | Debug mode (0/1)                  | No       | 0       |
| `PORT`                | Server port (auto-set by Railway) | No       | -       |
| `WEB_CONCURRENCY`     | Gunicorn workers                  | No       | 2       |

## Post-Deployment

1. **Test your deployment**:

   - Visit your Railway-provided URL
   - Check the `/health` endpoint: `https://your-app.railway.app/health`

2. **Monitor logs**:

   - In Railway dashboard, go to "Deployments" → "View Logs"
   - Or use CLI: `railway logs`

3. **Set up custom domain** (optional):
   - Go to "Settings" → "Domains"
   - Add your custom domain
   - Update DNS records as instructed

## Troubleshooting

### App won't start

- Check logs: `railway logs`
- Verify all required environment variables are set
- Ensure `Procfile` is correct

### 500 errors

- Check that API keys are valid
- Review application logs for errors
- Verify environment variables are set correctly

### Port binding issues

- Railway automatically sets `PORT` environment variable
- Your `Procfile` uses `$PORT` correctly
- The app will bind to `0.0.0.0:$PORT`

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
