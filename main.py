import os
import logging
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

def analyze_sentiment(text):
    """
    Analyze sentiment using TextBlob
    Returns polarity, subjectivity, and sentiment classification with additional metrics
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Classify sentiment based on polarity
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    # Calculate confidence level
    confidence = abs(polarity)
    if confidence > 0.7:
        confidence_level = "Very High"
    elif confidence > 0.3:
        confidence_level = "High"
    elif confidence > 0.1:
        confidence_level = "Moderate"
    else:
        confidence_level = "Low"
    
    # Additional text analysis
    word_count = len(text.split())
    char_count = len(text)
    
    return {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'sentiment': sentiment,
        'confidence': confidence,
        'confidence_level': confidence_level,
        'word_count': word_count,
        'char_count': char_count,
        'timestamp': datetime.now().isoformat()
    }

@app.route('/')
def index():
    """Homepage with text input form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process sentiment analysis and display results"""
    text = request.form.get('text', '').strip()
    
    # Validate input
    if not text:
        flash('Please enter some text to analyze.', 'error')
        return redirect(url_for('index'))
    
    # Check text length
    if len(text) > 5000:
        flash('Text is too long. Please limit to 5000 characters.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Perform sentiment analysis
        analysis = analyze_sentiment(text)
        
        return render_template('result.html', 
                             text=text,
                             polarity=analysis['polarity'],
                             subjectivity=analysis['subjectivity'],
                             sentiment=analysis['sentiment'])
    
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {e}")
        flash('An error occurred while analyzing the text. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for sentiment analysis"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Empty text provided'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
        
        # Perform sentiment analysis
        analysis = analyze_sentiment(text)
        
        return jsonify({
            'success': True,
            'data': analysis
        })
    
    except Exception as e:
        logging.error(f"API Error analyzing sentiment: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'sentiment-analysis-tool'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
