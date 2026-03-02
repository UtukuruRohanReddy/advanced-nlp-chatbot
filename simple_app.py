from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import random
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)
CORS(app)

class SimpleNLPChatbot:
    def __init__(self):
        self.download_nltk_data()
        self.initialize_sentiment_analyzer()
        self.initialize_responses()
        self.conversation_context = []
        
    def download_nltk_data(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
            
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')
    
    def initialize_sentiment_analyzer(self):
        self.sia = SentimentIntensityAnalyzer()
        
    def initialize_responses(self):
        self.responses = {
            'greetings': {
                'patterns': [
                    r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b',
                    r'\b(what\'s up|sup|howdy)\b'
                ],
                'responses': [
                    "Hello! How can I assist you today?",
                    "Hi there! What can I help you with?",
                    "Hey! How are you doing today?",
                    "Greetings! I'm here to help you.",
                    "Hi! Great to see you. What's on your mind?"
                ]
            },
            'how_are_you': {
                'patterns': [
                    r'\b(how are you|how do you do|how are you doing|what about you)\b',
                    r'\b(how\'s it going|how have you been)\b'
                ],
                'responses': [
                    "I'm doing great, thank you for asking! I'm ready to help you with anything you need.",
                    "I'm functioning perfectly! How can I assist you today?",
                    "All systems are running smoothly! What would you like to know?",
                    "I'm excellent! Ready to chat and help. What's on your mind?"
                ]
            },
            'capabilities': {
                'patterns': [
                    r'\b(what can you do|what do you do|capabilities|features|help|abilities)\b',
                    r'\b(what are you capable of|tell me about yourself)\b'
                ],
                'responses': [
                    "I'm an advanced NLP chatbot that can understand sentiment, engage in intelligent conversations, and provide helpful responses. I use NLTK for natural language processing!",
                    "My capabilities include sentiment analysis, intelligent conversation, question answering, and contextual understanding. I use advanced NLP techniques to better understand you!",
                    "I can analyze text sentiment, understand context, and provide meaningful responses. Try asking me questions, sharing your thoughts, or just having a conversation!"
                ]
            },
            'time_date': {
                'patterns': [
                    r'\b(what time|current time|time now|what time is it)\b',
                    r'\b(date today|what\'s the date|current date)\b',
                    r'\b(what day is it|what day today)\b'
                ],
                'responses': [
                    lambda: f"The current time is {datetime.now().strftime('%I:%M %p')} and today's date is {datetime.now().strftime('%A, %B %d, %Y')}.",
                    lambda: f"It's {datetime.now().strftime('%I:%M %p')} on {datetime.now().strftime('%A, %B %d')}.",
                    lambda: f"Right now it's {datetime.now().strftime('%I:%M %p')} on {datetime.now().strftime('%B %d, %Y')}."
                ]
            },
            'identity': {
                'patterns': [
                    r'\b(what is your name|who are you|your name|what should I call you)\b',
                    r'\b(what are you|tell me about yourself)\b'
                ],
                'responses': [
                    "I'm an Advanced NLP Chatbot powered by Python and NLTK. I can understand sentiment and engage in intelligent conversations. You can call me Assistant!",
                    "I'm your AI-powered chatbot assistant with advanced natural language processing capabilities. I use cutting-edge NLP techniques to understand and respond to you better!"
                ]
            },
            'thanks': {
                'patterns': [
                    r'\b(thank you|thanks|appreciate|helpful|good job|well done)\b',
                    r'\b(thanks a lot|thank you so much|grateful)\b'
                ],
                'responses': [
                    "You're very welcome! I'm glad I could help you. Is there anything else you need assistance with?",
                    "Happy to help! Feel free to ask if you need anything else.",
                    "You're welcome! I'm always here to help whenever you need me.",
                    "My pleasure! I'm here to assist you with whatever you need."
                ]
            },
            'goodbye': {
                'patterns': [
                    r'\b(goodbye|bye|see you|farewell|exit|quit|leave)\b',
                    r'\b(talk to you later|catch you later|see ya)\b'
                ],
                'responses': [
                    "Goodbye! It was great chatting with you. Feel free to come back anytime you need help!",
                    "See you later! Have a wonderful day!",
                    "Farewell! I'm here whenever you need assistance again.",
                    "Take care! Looking forward to our next conversation!"
                ]
            }
        }
    
    def analyze_sentiment(self, text):
        sentiment_scores = self.sia.polarity_scores(text)
        compound_score = sentiment_scores['compound']
        
        if compound_score >= 0.05:
            return 'positive', sentiment_scores
        elif compound_score <= -0.05:
            return 'negative', sentiment_scores
        else:
            return 'neutral', sentiment_scores
    
    def preprocess_text(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
        return ' '.join(tokens)
    
    def get_response(self, user_input):
        self.conversation_context.append({'user': user_input, 'timestamp': datetime.now().isoformat()})
        
        # Analyze sentiment
        sentiment, sentiment_scores = self.analyze_sentiment(user_input)
        
        # Preprocess text for pattern matching
        processed_text = self.preprocess_text(user_input)
        
        # Pattern matching for categories
        for category, data in self.responses.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_input, re.IGNORECASE):
                    responses = data['responses']
                    if callable(responses[0]):
                        response_text = responses[0]()
                    else:
                        response_text = random.choice(responses)
                    
                    return {
                        'response': response_text,
                        'sentiment': sentiment,
                        'sentiment_scores': sentiment_scores,
                        'entities': [],
                        'confidence': 0.9
                    }
        
        # Default response
        default_responses = [
            "That's interesting! Could you tell me more about that?",
            "I'm not sure I understand completely. Could you rephrase that?",
            "That's a great question! Let me think about how I can best help you with that.",
            "I appreciate your question. While I may not have a specific answer, I'm here to chat and help in any way I can.",
            "Tell me more about what you're interested in, and I'll do my best to assist you!"
        ]
        
        return {
            'response': random.choice(default_responses),
            'sentiment': sentiment,
            'sentiment_scores': sentiment_scores,
            'entities': [],
            'confidence': 0.3
        }

# Initialize the chatbot
chatbot = SimpleNLPChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from the chatbot
        bot_response = chatbot.get_response(user_message)
        
        return jsonify(bot_response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("Starting NLP Chatbot Server...")
    print("Server will be available at: http://localhost:5000")
    print("Chatbot with NLTK sentiment analysis is ready!")
    app.run(debug=True, host='0.0.0.0', port=5000)
