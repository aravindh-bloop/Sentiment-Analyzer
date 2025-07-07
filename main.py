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

# Global list to store comment history
comment_history = []

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
    Suggest improvements to make text more positive using word replacement
    """
    # Dictionary of negative to positive word replacements
    word_replacements = {
        # Negative words
        'bad': 'good',
        'terrible': 'excellent',
        'awful': 'wonderful',
        'horrible': 'amazing',
        'hate': 'love',
        'worst': 'best',
        'ugly': 'beautiful',
        'boring': 'interesting',
        'stupid': 'smart',
        'useless': 'useful',
        'broken': 'working',
        'fail': 'succeed',
        'failed': 'succeeded',
        'failure': 'success',
        'disappointing': 'satisfying',
        'disappointed': 'satisfied',
        'annoying': 'pleasant',
        'frustrated': 'pleased',
        'angry': 'happy',
        'sad': 'happy',
        'unhappy': 'happy',
        'difficult': 'easy',
        'hard': 'easy',
        'impossible': 'possible',
        'never': 'always',
        'problem': 'solution',
        'problems': 'solutions',
        'issues': 'features',
        'complain': 'appreciate',
        'complained': 'appreciated',
        'complaining': 'appreciating',
        
        # Neutral to positive
        'okay': 'great',
        'fine': 'excellent',
        'average': 'outstanding',
        'normal': 'exceptional',
        'decent': 'fantastic',
        'adequate': 'perfect',
        
        # Intensifiers
        'not good': 'excellent',
        'not bad': 'really good',
        'not great': 'fantastic',
        'could be better': 'is amazing',
        'needs improvement': 'is wonderful',
        'waste of time': 'valuable experience',
        'waste of money': 'great investment',
        'regret': 'appreciate',
        'mistake': 'good decision',
        'wrong': 'right',
        'incorrect': 'perfect',
        'poor': 'excellent',
        'weak': 'strong',
        'slow': 'fast',
        'expensive': 'worth every penny',
        'cheap': 'affordable and great',
        'small': 'perfectly sized',
        'too much': 'just right',
        'too little': 'perfectly adequate',
        'confusing': 'clear and easy',
        'complicated': 'comprehensive',
        'overwhelming': 'feature-rich'
    }
    
    # Convert to lowercase for matching, but preserve original case
    words = text.split()
    improved_words = []
    changes_made = []
    
    for word in words:
        # Remove punctuation for matching
        clean_word = word.lower().strip('.,!?;:"()[]{}')
        
        if clean_word in word_replacements:
            # Replace while preserving punctuation
            punctuation = ''.join(c for c in word if not c.isalnum())
            replacement = word_replacements[clean_word]
            
            # Preserve capitalization
            if word[0].isupper():
                replacement = replacement.capitalize()
            
            new_word = replacement + punctuation
            improved_words.append(new_word)
            changes_made.append((word, new_word))
        else:
            improved_words.append(word)
    
    improved_text = ' '.join(improved_words)
    
    # Additional positive phrases to add
    positive_additions = [
        "I really appreciate",
        "This is fantastic",
        "Absolutely love",
        "Highly recommend",
        "Outstanding quality",
        "Exceeded expectations",
        "Wonderful experience",
        "Brilliant work",
        "Perfect solution",
        "Amazing results"
    ]
    
    # If no changes were made, add a positive prefix
    if not changes_made:
        import random
        positive_prefix = random.choice(positive_additions)
        improved_text = f"{positive_prefix} how {improved_text.lower()}"
        changes_made.append(("Added positive tone", positive_prefix))
    
    return {
        'improved_text': improved_text,
        'changes_made': changes_made,
        'original_text': text
    }

@app.route('/')
def index():
    """Homepage with text input form"""
    return render_template('index.html', comment_history=comment_history)

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
        
        # Store in global history with unique ID
        comment_id = len(comment_history) + 1
        comment_entry = {
            'id': comment_id,
            'text': text,
            'polarity': analysis['polarity'],
            'subjectivity': analysis['subjectivity'],
            'sentiment': analysis['sentiment'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'word_count': analysis['word_count'],
            'char_count': analysis['char_count']
        }
        
        comment_history.append(comment_entry)
        
        return render_template('result.html', 
                             text=text,
                             polarity=analysis['polarity'],
                             subjectivity=analysis['subjectivity'],
                             sentiment=analysis['sentiment'],
                             comment_history=comment_history)
    
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
        # Find the comment in history
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
    return render_template('history.html', comment_history=comment_history)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear all comment history"""
    global comment_history
    comment_history = []
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

