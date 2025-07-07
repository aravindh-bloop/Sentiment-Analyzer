# Sentiment Analysis Tool - Deployment Guide

## Overview
This is a complete Flask-based sentiment analysis application with AI-powered text improvement using DeepSeek API via OpenRouter.

## Features
- **Sentiment Analysis**: Real-time sentiment classification using TextBlob
- **AI Text Improvement**: DeepSeek AI enhances negative text while preserving meaning
- **Session-based History**: Individual user comment history without login
- **Beautiful UI**: Bootstrap-based responsive design
- **Multiple Deployment Options**: Replit, Render, Heroku, local development

## Quick Start

### 1. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable (optional for basic features)
export DEEPSEEK_API_KEY="your-openrouter-api-key"

# Run the application
python run.py
```

### 2. Render Deployment (Recommended)
1. **Upload to GitHub**:
   - Create a new repository
   - Upload all files from this package
   - Commit and push

2. **Deploy on Render**:
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Select "Web Service"
   - Use these settings:
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn --bind 0.0.0.0:$PORT main:app`
   - Add Environment Variable: `DEEPSEEK_API_KEY` with your OpenRouter API key

### 3. Replit Deployment
1. Import this project to Replit
2. Add `DEEPSEEK_API_KEY` to Replit Secrets
3. Run the project

## API Key Setup

### Getting DeepSeek API Key (via OpenRouter)
1. Go to [openrouter.ai](https://openrouter.ai)
2. Create an account and sign in
3. Go to "Keys" section
4. Generate a new API key
5. Add credits to your account
6. Use the key in your environment variables

## File Structure
```
sentiment-analysis-tool/
├── main.py                    # Main Flask application
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python version for deployment
├── Procfile                  # Web service command
├── render.yaml               # Render configuration
├── templates/                # HTML templates
│   ├── index.html           # Homepage
│   ├── result.html          # Analysis results
│   ├── review.html          # Text improvement
│   └── history.html         # Comment history
├── install.py               # Dependency installer
├── run.py                   # Application runner
├── run.sh                   # Unix launcher
├── run.bat                  # Windows launcher
├── deploy.py                # Deployment helper
├── README.md                # Documentation
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore file
```

## Environment Variables
- `DEEPSEEK_API_KEY`: OpenRouter API key for AI text improvement (optional)
- `SESSION_SECRET`: Flask session secret (auto-generated if not provided)

## Troubleshooting

### Common Issues
1. **"Module not found" errors**: Install dependencies with `pip install -r requirements.txt`
2. **API not working**: Check your OpenRouter API key and account balance
3. **Deployment fails**: Ensure all files are uploaded and environment variables are set

### Support
- Check the logs in your deployment platform
- Verify all files are present in your repository
- Ensure environment variables are properly set

## Features in Detail

### Sentiment Analysis
- Uses TextBlob for accurate sentiment classification
- Provides polarity (-1 to 1) and subjectivity (0 to 1) scores
- Classifies text as Positive, Negative, or Neutral

### AI Text Improvement
- Powered by DeepSeek AI via OpenRouter
- Preserves original meaning while improving tone
- Makes minimal, natural changes to negative text
- Falls back to basic improvements if API is unavailable

### Session Management
- Individual user history without requiring login
- Privacy-focused: each user's data is isolated
- Comment history persists during browser session

## Version History
- v1.0: Basic sentiment analysis with TextBlob
- v2.0: Added UI enhancements and interactive features
- v3.0: Session-based history and AI-powered improvements
- v4.0: DeepSeek integration and deployment optimization

## License
MIT License - See LICENSE file for details