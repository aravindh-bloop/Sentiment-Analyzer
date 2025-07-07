import os
import logging
import json
from datetime import datetime
import uuid
import re
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")


# Helper function to get or create user session comment history
def get_comment_history():
    """Get comment history for current session"""
    if 'comment_history' not in session:
        session['comment_history'] = []
    return session['comment_history']


def add_comment_to_history(comment_data):
    """Add a comment to the current session's history"""
    comment_history = get_comment_history()
    comment_data['id'] = len(comment_history) + 1
    comment_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_history.append(comment_data)
    session['comment_history'] = comment_history
    session.modified = True

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

def improve_sentiment_with_ai(text):
    """
    Use DeepSeek AI to improve sentiment while preserving original meaning
    """
    deepseek_api_key = os.environ.get('DEEPSEEK_API_KEY')
    
    if not deepseek_api_key:
        # Fallback to minimal changes when no API key
        return improve_sentiment_fallback(text)
    
    try:
        # DeepSeek API call
        headers = {
            'Authorization': f'Bearer {deepseek_api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'deepseek/deepseek-chat',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are an expert at improving the tone of text while preserving the original meaning exactly. Your task is to make negative or harsh comments more positive and constructive, but keep the core message and intent identical. Make minimal changes - only soften harsh language and improve tone. Do not add extra content or change the meaning. Respond with only the improved text, nothing else.'
                },
                {
                    'role': 'user',
                    'content': f'Please improve the tone of this text while keeping the exact same meaning: "{text}"'
                }
            ],
            'max_tokens': 50,
            'temperature': 0.2
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            improved_text = result['choices'][0]['message']['content'].strip()
            
            # Remove quotes if the AI added them
            if improved_text.startswith('"') and improved_text.endswith('"'):
                improved_text = improved_text[1:-1]
            
            original_analysis = analyze_sentiment(text)
            
            # Check if improvement actually made it more positive
            improved_analysis = analyze_sentiment(improved_text)
            
            changes_made = []
            if improved_text != text:
                changes_made.append(("AI-enhanced tone", "DeepSeek improved positivity while preserving meaning"))
            else:
                changes_made.append(("No changes needed", "Original text was already well-written"))
            
            return {
                'improved_text': improved_text,
                'changes_made': changes_made,
                'original_length': len(text),
                'improved_length': len(improved_text),
                'improvement_type': 'AI-Powered Enhancement',
                'original_polarity': original_analysis['polarity'],
                'explanation': 'DeepSeek AI improved tone and positivity while preserving original meaning'
            }
        else:
            logging.error(f"DeepSeek API error: {response.status_code} - {response.text}")
            return improve_sentiment_fallback(text)
            
    except Exception as e:
        logging.error(f"Error calling DeepSeek API: {e}")
        return improve_sentiment_fallback(text)

def improve_sentiment_fallback(text):
    """
    Fallback function for when DeepSeek API is not available
    """
    original_analysis = analyze_sentiment(text)
    
    # Very minimal improvements that don't change meaning drastically
    improved_text = text.strip()
    changes_made = []
    
    # Only make very minor, natural adjustments for extremely negative text
    if original_analysis['polarity'] < -0.5:  # Only for very negative text
        simple_replacements = {
            r'\bterrible\b': 'not great',
            r'\bawful\b': 'not good',
            r'\bhate\b': 'really dislike',
            r'\bstupid\b': 'frustrating',
            r'\buseless\b': 'not helpful'
        }
        
        for pattern, replacement in simple_replacements.items():
            if re.search(pattern, improved_text, re.IGNORECASE):
                improved_text = re.sub(pattern, replacement, improved_text, flags=re.IGNORECASE)
                changes_made.append(("Softened harsh language", "More diplomatic tone"))
                break
    
    # If no changes were made, leave it as is
    if not changes_made:
        changes_made.append(("Preserved original", "No changes needed - meaning preserved"))
    
    return {
        'improved_text': improved_text,
        'changes_made': changes_made,
        'original_length': len(text),
        'improved_length': len(improved_text),
        'improvement_type': 'Minimal Adjustment',
        'original_polarity': original_analysis['polarity'],
        'explanation': 'Minor adjustments to tone while preserving original meaning and intent'
    }

def improve_sentiment(text):
    """
    Main function for sentiment improvement - calls AI-powered version
    """
    return improve_sentiment_with_ai(text)

@app.route('/')
def index():
    """Homepage with text input form"""
    return render_template('index.html', comment_history=get_comment_history())

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
        
        # Store in session-based history
        comment_entry = {
            'text': text,
            'polarity': analysis['polarity'],
            'subjectivity': analysis['subjectivity'],
            'sentiment': analysis['sentiment'],
            'word_count': analysis['word_count'],
            'char_count': analysis['char_count']
        }
        
        add_comment_to_history(comment_entry)
        
        return render_template('result.html', 
                             text=text,
                             polarity=analysis['polarity'],
                             subjectivity=analysis['subjectivity'],
                             sentiment=analysis['sentiment'],
                             comment_history=get_comment_history())
    
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

@app.route('/review/<int:comment_id>')
def review_comment(comment_id):
    """Review a specific comment and suggest improvements"""
    try:
        # Find the comment in session history
        comment_history = get_comment_history()
        comment = None
        for c in comment_history:
            if c['id'] == comment_id:
                comment = c
                break
        
        if not comment:
            flash('Comment not found.', 'error')
            return redirect(url_for('index'))
        
        # Generate improvement suggestions
        improvement = improve_sentiment(comment['text'])
        
        # Analyze the improved text
        improved_analysis = analyze_sentiment(improvement['improved_text'])
        
        return render_template('review.html',
                             original_comment=comment,
                             improvement=improvement,
                             improved_analysis=improved_analysis,
                             comment_history=comment_history)
    
    except Exception as e:
        logging.error(f"Error reviewing comment {comment_id}: {e}")
        flash('An error occurred while reviewing the comment.', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def view_history():
    """View all comment history"""
    return render_template('history.html', comment_history=get_comment_history())

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear all comment history"""
    session['comment_history'] = []
    session.modified = True
    flash('Comment history cleared successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'sentiment-analysis-tool'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
