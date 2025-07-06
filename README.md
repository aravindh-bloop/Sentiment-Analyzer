# Sentiment Analysis Tool

A beautiful, modern Flask-based web application that performs sentiment analysis on user-entered text using TextBlob. The application features an intuitive interface with advanced styling, interactive elements, and comprehensive sentiment analysis capabilities.

## Features

### 🎯 Core Functionality
- **Sentiment Analysis**: Classify text as Positive, Negative, or Neutral
- **Polarity Scoring**: Range from -1 (very negative) to +1 (very positive)
- **Subjectivity Analysis**: Range from 0 (objective) to 1 (subjective)
- **Confidence Levels**: Visual indicators of analysis confidence

### 🎨 Enhanced UI/UX
- **Beautiful Design**: Modern gradient backgrounds and card-based layout
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **Sample Text Buttons**: Quick-start with positive, negative, and neutral examples
- **Character Counter**: Real-time character count with color-coded warnings
- **Responsive Design**: Works perfectly on desktop and mobile devices

### 📊 Advanced Features
- **Analysis Summary**: Detailed interpretation of results
- **Word & Character Count**: Comprehensive text metrics
- **Export Functionality**: Download results as JSON
- **Share Results**: Copy analysis results to clipboard
- **Analysis Counter**: Track number of analyses performed
- **API Endpoint**: RESTful API for programmatic access

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Start

1. **Download the project files**
   ```bash
   # Extract the project to your desired directory
   cd sentiment-analysis-tool
   ```

2. **Install dependencies**
   ```bash
   pip install Flask TextBlob gunicorn
   ```

3. **Download language corpora (first time only)**
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

### Alternative Setup with Requirements

If you have a `requirements.txt` file:
```bash
pip install -r requirements.txt
python main.py
```

## Usage

### Web Interface
1. Visit the homepage
2. Enter text in the textarea (up to 5000 characters)
3. Use sample text buttons for quick testing
4. Click "Analyze Sentiment" to get results
5. View detailed analysis including:
   - Sentiment classification
   - Polarity and subjectivity scores
   - Confidence levels
   - Analysis summary

### API Usage

Send POST requests to `/api/analyze`:

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

Response:
```json
{
  "success": true,
  "data": {
    "polarity": 0.5,
    "subjectivity": 0.6,
    "sentiment": "Positive",
    "confidence": 0.5,
    "confidence_level": "High",
    "word_count": 4,
    "char_count": 19,
    "timestamp": "2025-07-05T18:35:50"
  }
}
```

## Project Structure

```
sentiment-analysis-tool/
├── main.py                 # Main Flask application
├── templates/
│   ├── index.html         # Homepage with input form
│   └── result.html        # Results display page
├── README.md              # This file
├── replit.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## Deployment

### Local Development
```bash
python main.py
```

### Production with Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Environment Variables
- `SESSION_SECRET`: Flask session secret key (defaults to "dev-secret-key")
- `PORT`: Port number (defaults to 5000)

## Technical Details

### Technologies Used
- **Backend**: Flask (Python web framework)
- **NLP**: TextBlob for sentiment analysis
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5 with custom CSS
- **Icons**: Font Awesome 6.0

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)

### Performance
- Lightweight and fast
- No database required
- Stateless application
- Minimal resource usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue in the repository

## Version History

- **v1.0.0** (2025-07-05): Initial release with full functionality
  - Basic sentiment analysis
  - Beautiful UI/UX
  - API endpoint
  - Export/share features
  - Sample text integration
  - Responsive design

## Acknowledgments

- TextBlob library for natural language processing
- Bootstrap for responsive design
- Font Awesome for icons
- Flask framework for web development