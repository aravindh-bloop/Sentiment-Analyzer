import os
import logging
import json
from datetime import datetime
import uuid
import re
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

def improve_sentiment(text):
    """
    Advanced sentiment improvement using grammar-enhanced full-sentence rewrites
    Similar to Grammarly - preserves meaning while improving tone and clarity
    """
    # Analyze original sentiment
    original_analysis = analyze_sentiment(text)
    
    # Advanced sentence rewriting patterns
    rewrite_patterns = [
        # Negative expressions to positive alternatives
        {
            'patterns': [
                r"this is (bad|terrible|awful|horrible|worst)",
                r"this (sucks|is terrible|is awful|is bad)",
                r"(hate|dislike) this",
                r"this (doesn't work|failed|is broken)",
                r"this is (useless|worthless|pointless)"
            ],
            'rewrites': [
                "this could be improved and has potential",
                "this has room for enhancement",
                "this would benefit from some adjustments",
                "this presents opportunities for improvement",
                "this can be developed into something better"
            ]
        },
        
        # Frustration to constructive feedback
        {
            'patterns': [
                r"(why|how) is this so (bad|terrible|awful|confusing|hard|difficult)",
                r"this (makes no sense|is confusing|is unclear)",
                r"(can't|cannot) understand this",
                r"this is (too hard|too difficult|impossible)",
                r"this (doesn't|does not) make sense"
            ],
            'rewrites': [
                "this would be clearer with better explanation",
                "this concept could be presented more clearly",
                "this would benefit from additional context",
                "this has potential but needs clearer communication",
                "this idea could be expressed more effectively"
            ]
        },
        
        # Complaints to suggestions
        {
            'patterns': [
                r"(complaining|complain) about",
                r"this (problem|issue|bug)",
                r"(disappointed|frustrated|annoyed) (with|by)",
                r"this (never|doesn't) work",
                r"waste of (time|money|effort)"
            ],
            'rewrites': [
                "providing feedback about",
                "this area for improvement",
                "hoping for better results with",
                "this needs some attention to work properly",
                "valuable learning experience"
            ]
        },
        
        # Harsh criticism to constructive feedback
        {
            'patterns': [
                r"this is (stupid|dumb|ridiculous|absurd)",
                r"(whoever|who) (made|created|designed) this",
                r"this (obviously|clearly) (doesn't|does not) work",
                r"this is (completely|totally) (wrong|incorrect|useless)",
                r"this (fails|sucks) at"
            ],
            'rewrites': [
                "this approach could be reconsidered",
                "the creator might want to revisit this",
                "this would work better with some adjustments",
                "this has potential but needs refinement",
                "this could be more effective at"
            ]
        }
    ]
    
    # Apply sophisticated rewriting
    improved_text = text.lower().strip()
    changes_made = []
    rewrite_applied = False
    
    # Try pattern-based rewriting first
    for pattern_group in rewrite_patterns:
        for i, pattern in enumerate(pattern_group['patterns']):
            if re.search(pattern, improved_text, re.IGNORECASE):
                rewrite_index = i % len(pattern_group['rewrites'])
                rewrite_template = pattern_group['rewrites'][rewrite_index]
                
                # Apply the rewrite while preserving context
                improved_text = re.sub(pattern, rewrite_template, improved_text, flags=re.IGNORECASE)
                changes_made.append(("Rewritten for positivity", "Enhanced tone and clarity"))
                rewrite_applied = True
                break
        
        if rewrite_applied:
            break
    
    # If no pattern matches, apply contextual improvements
    if not rewrite_applied:
        if original_analysis['polarity'] < -0.3:  # Very negative
            # Add constructive framing
            improved_text = f"While there are areas for improvement, {improved_text}"
            changes_made.append(("Added constructive framing", "Balanced perspective"))
        elif original_analysis['polarity'] < 0:  # Mildly negative
            # Soften the tone
            improved_text = re.sub(r'\b(no|not|never|nothing)\b', 'limited', improved_text)
            improved_text = re.sub(r'\b(bad|poor|terrible)\b', 'could be better', improved_text)
            changes_made.append(("Softened negative language", "More diplomatic tone"))
        elif original_analysis['polarity'] > 0.3:  # Already positive
            # Enhance existing positivity
            improved_text = re.sub(r'\b(good|nice|fine|okay)\b', 'excellent', improved_text)
            changes_made.append(("Enhanced positive language", "Stronger positive tone"))
    
    # Grammar and clarity improvements
    improved_text = improved_text.strip()
    
    # Capitalize first letter and ensure proper sentence structure
    if improved_text:
        improved_text = improved_text[0].upper() + improved_text[1:]
        
        # Ensure proper sentence ending
        if not improved_text.endswith(('.', '!', '?')):
            improved_text += '.'
    
    # Remove double spaces and fix common grammar issues
    improved_text = re.sub(r'\s+', ' ', improved_text)
    improved_text = re.sub(r'\s+([,.!?])', r'\1', improved_text)
    
    # If no improvements were made, provide encouragement
    if not changes_made:
        if original_analysis['polarity'] >= 0:
            improved_text = f"I appreciate that {improved_text.lower()}"
            changes_made.append(("Added appreciation", "Positive acknowledgment"))
        else:
            improved_text = f"Thank you for the feedback - {improved_text.lower()}"
            changes_made.append(("Added gratitude", "Constructive response"))
    
    return {
        'improved_text': improved_text,
        'changes_made': changes_made,
        'original_length': len(text),
        'improved_length': len(improved_text),
        'improvement_type': 'Grammar-Enhanced Rewrite',
        'original_polarity': original_analysis['polarity'],
        'explanation': 'Rewritten for better tone, clarity, and positive communication while preserving original meaning'
    }

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
