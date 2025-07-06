# Sentiment Analysis Tool

## Overview

This is a Flask-based web application that performs sentiment analysis on user-provided text using the TextBlob library. The application provides a simple, user-friendly interface for analyzing text sentiment, polarity, and subjectivity through natural language processing.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating engine)
- **UI Framework**: Bootstrap 5 with dark theme via CDN
- **Icons**: Font Awesome 6.0 for enhanced visual elements
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

### Backend Architecture
- **Web Framework**: Flask (Python micro-framework)
- **NLP Library**: TextBlob for sentiment analysis
- **Session Management**: Flask's built-in session handling with secret key
- **Error Handling**: Flash messages for user feedback

### Application Structure
```
/
├── main.py              # Main Flask application
├── templates/
│   ├── index.html       # Homepage with input form
│   └── result.html      # Results display page (partial)
```

## Key Components

### 1. Sentiment Analysis Engine
- **Library**: TextBlob - chosen for its simplicity and accuracy in basic sentiment analysis
- **Metrics Calculated**:
  - Polarity: Range from -1 (negative) to 1 (positive)
  - Subjectivity: Range from 0 (objective) to 1 (subjective)
  - Sentiment Classification: Positive, Negative, or Neutral

### 2. Web Interface
- **Input Form**: Large textarea for text input with Bootstrap styling
- **Results Display**: Structured presentation of analysis results
- **Flash Messages**: User feedback system for errors and notifications

### 3. Route Handlers
- **GET /**: Homepage displaying input form
- **POST /analyze**: Processes text analysis and returns results

## Data Flow

1. User enters text on homepage (`/`)
2. Form submission triggers POST request to `/analyze`
3. Input validation ensures text is provided
4. TextBlob processes the text for sentiment analysis
5. Results are calculated (polarity, subjectivity, classification)
6. Results are displayed on results page with formatted output

## External Dependencies

### Python Libraries
- **Flask**: Web framework for handling HTTP requests and responses
- **TextBlob**: Natural language processing library for sentiment analysis

### Frontend Dependencies (CDN)
- **Bootstrap 5**: UI framework for responsive design and components
- **Font Awesome 6.0**: Icon library for enhanced visual elements

### Environment Variables
- **SESSION_SECRET**: Flask session secret key (defaults to "dev-secret-key")

## Deployment Strategy

### Configuration
- **Debug Mode**: Enabled via `logging.basicConfig(level=logging.DEBUG)`
- **Secret Key**: Configurable via environment variable for production security
- **Static Assets**: Served via CDN for improved performance

### Hosting Considerations
- No database requirements - stateless application
- Minimal resource requirements
- Environment variable configuration for production deployment

## Changelog

- July 05, 2025. Initial setup - Basic Flask application with TextBlob sentiment analysis
- July 05, 2025. Major UI/UX Enhancement - Added beautiful gradient design, interactive elements, sample text buttons, character counter, confidence meters, and advanced styling
- July 05, 2025. Feature Expansion - Added API endpoint, export functionality, share results, analysis summary, and enhanced metrics
- July 05, 2025. Package Preparation - Created complete downloadable package with installation scripts, documentation, and cross-platform compatibility

## Additional Features Added

### Enhanced User Interface
- **Gradient Design**: Beautiful gradient backgrounds and card-based layouts
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **Sample Text Buttons**: Quick-start with positive, negative, and neutral examples
- **Character Counter**: Real-time character count with color-coded warnings (5000 char limit)
- **Confidence Meters**: Visual confidence indicators based on polarity strength
- **Analysis Counter**: Persistent counter tracking analyses performed using localStorage

### Advanced Functionality
- **API Endpoint**: RESTful API at `/api/analyze` for programmatic access
- **Export Results**: Download analysis results as JSON files
- **Share Results**: Copy analysis results to clipboard or use native share API
- **Enhanced Metrics**: Word count, character count, confidence levels, and detailed interpretations
- **Health Check**: System health monitoring endpoint at `/health`

### Cross-Platform Package
- **README.md**: Comprehensive documentation with setup instructions
- **install.py**: Automated dependency installation script
- **run.py**: Standalone application runner with logging
- **run.sh**: Unix/Linux launcher script
- **run.bat**: Windows batch file launcher
- **LICENSE**: MIT License for open source distribution
- **.gitignore**: Git ignore file for clean repository management

### Technical Enhancements
- **Input Validation**: Text length limits and error handling
- **Responsive Design**: Mobile-first approach with Bootstrap grid system
- **Performance Optimizations**: Efficient animations and smooth interactions
- **Cross-Browser Compatibility**: Support for modern browsers and mobile devices

## User Preferences

Preferred communication style: Simple, everyday language.