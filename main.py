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
    Advanced sentiment improvement using natural language rewriting
    Creates meaningful, grammatically correct positive alternatives
    """
    # Analyze original sentiment
    original_analysis = analyze_sentiment(text)
    original_text = text.strip()
    
    # Smart rewriting patterns that preserve meaning while improving tone
    rewrite_rules = [
        # Direct negative statements
        {
            'pattern': r'^(this is|it is|that is) (bad|terrible|awful|horrible|worst|useless|pointless|stupid|dumb)(.*)$',
            'rewrite': lambda m: f"This could be improved{m.group(3) if m.group(3) else ''}.",
            'explanation': 'Converted harsh criticism to constructive feedback'
        },
        
        # Frustration expressions
        {
            'pattern': r'^(i hate|i dislike|i can\'t stand) (.+)$',
            'rewrite': lambda m: f"I would prefer if {m.group(2)} were different.",
            'explanation': 'Transformed strong dislike into preference'
        },
        
        # Failure statements  
        {
            'pattern': r'^(this|it) (doesn\'t work|failed|is broken|never works)(.*)$',
            'rewrite': lambda m: f"This needs some adjustments to work properly{m.group(3) if m.group(3) else ''}.",
            'explanation': 'Reframed failure as opportunity for improvement'
        },
        
        # Confusion expressions
        {
            'pattern': r'^(this|it) (makes no sense|is confusing|is unclear|doesn\'t make sense)(.*)$',
            'rewrite': lambda m: f"This could be explained more clearly{m.group(3) if m.group(3) else ''}.",
            'explanation': 'Turned confusion into request for clarity'
        },
        
        # Waste expressions
        {
            'pattern': r'^(this is a |it\'s a )?(waste of time|waste of money|waste of effort)(.*)$',
            'rewrite': lambda m: f"This could be a more valuable use of resources{m.group(3) if m.group(3) else ''}.",
            'explanation': 'Reframed waste as potential value'
        },
        
        # Impossibility claims
        {
            'pattern': r'^(this is|it is) (impossible|too hard|too difficult)(.*)$',
            'rewrite': lambda m: f"This is challenging but achievable with the right approach{m.group(3) if m.group(3) else ''}.",
            'explanation': 'Turned impossibility into achievable challenge'
        },
        
        # Disappointment
        {
            'pattern': r'^(i am |i\'m )?(disappointed|frustrated|annoyed) (with|by) (.+)$',
            'rewrite': lambda m: f"I was hoping for better results from {m.group(4)}.",
            'explanation': 'Expressed disappointment as hope for improvement'
        },
        
        # Quality complaints
        {
            'pattern': r'^(the quality is|quality is) (poor|bad|terrible|awful)(.*)$',
            'rewrite': lambda m: f"The quality could be enhanced{m.group(3) if m.group(3) else ''}.",
            'explanation': 'Reframed poor quality as improvement opportunity'
        }
    ]
    
    improved_text = original_text
    changes_made = []
    rewrite_applied = False
    
    # Apply rewriting rules
    for rule in rewrite_rules:
        pattern = rule['pattern']
        match = re.search(pattern, improved_text, re.IGNORECASE)
        
        if match:
            if callable(rule['rewrite']):
                improved_text = rule['rewrite'](match)
            else:
                improved_text = rule['rewrite']
            
            changes_made.append(("Original phrase", rule['explanation']))
            rewrite_applied = True
            break
    
    # If no specific pattern matched, apply contextual improvements
    if not rewrite_applied:
        if original_analysis['polarity'] < -0.5:  # Very negative
            # Strong negative sentiment - provide balanced perspective
            improved_text = f"While there are areas that could be improved, {original_text.lower()}"
            changes_made.append(("Added balanced perspective", "Provided constructive framing"))
            
        elif original_analysis['polarity'] < -0.1:  # Mildly negative
            # Soften negative words
            negative_replacements = {
                r'\b(no|not|never)\b': 'limited',
                r'\b(bad|poor)\b': 'could be better',
                r'\b(hard|difficult)\b': 'challenging',
                r'\b(wrong|incorrect)\b': 'not quite right',
                r'\b(slow)\b': 'could be faster',
                r'\b(expensive)\b': 'an investment'
            }
            
            for pattern, replacement in negative_replacements.items():
                if re.search(pattern, improved_text, re.IGNORECASE):
                    improved_text = re.sub(pattern, replacement, improved_text, flags=re.IGNORECASE)
                    changes_made.append(("Softened negative language", "More diplomatic tone"))
                    break
                    
        elif original_analysis['polarity'] > 0.3:  # Already positive
            # Enhance existing positivity
            positive_enhancements = {
                r'\b(good|nice|fine|okay)\b': 'excellent',
                r'\b(great)\b': 'outstanding',
                r'\b(like)\b': 'really appreciate',
                r'\b(works)\b': 'works perfectly'
            }
            
            for pattern, enhancement in positive_enhancements.items():
                if re.search(pattern, improved_text, re.IGNORECASE):
                    improved_text = re.sub(pattern, enhancement, improved_text, flags=re.IGNORECASE)
                    changes_made.append(("Enhanced positive language", "Stronger positive tone"))
                    break
        
        elif original_analysis['polarity'] >= -0.1:  # Neutral
            # Add appreciation to neutral comments
            improved_text = f"I appreciate that {original_text.lower()}"
            changes_made.append(("Added appreciation", "Positive acknowledgment"))
    
    # Grammar and formatting improvements
    improved_text = improved_text.strip()
    
    # Ensure proper capitalization
    if improved_text and improved_text[0].islower():
        improved_text = improved_text[0].upper() + improved_text[1:]
    
    # Ensure proper sentence ending
    if improved_text and not improved_text.endswith(('.', '!', '?')):
        improved_text += '.'
    
    # Clean up spacing and punctuation
    improved_text = re.sub(r'\s+', ' ', improved_text)
    improved_text = re.sub(r'\s+([,.!?])', r'\1', improved_text)
    
    # If no changes were made, provide encouragement
    if not changes_made:
        if original_analysis['polarity'] >= 0:
            improved_text = f"I appreciate that {original_text.lower()}"
            changes_made.append(("Added appreciation", "Positive acknowledgment"))
        else:
            improved_text = f"Thank you for sharing your thoughts - {original_text.lower()}"
            changes_made.append(("Added gratitude", "Constructive response"))
    
    return {
        'improved_text': improved_text,
        'changes_made': changes_made,
        'original_length': len(original_text),
        'improved_length': len(improved_text),
        'improvement_type': 'Natural Language Rewrite',
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
