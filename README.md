# Advanced NLP Chatbot with Python Backend

A sophisticated chatbot with Natural Language Processing capabilities, featuring both frontend and Python backend integration for advanced NLP processing.

## Features

### 🤖 **Advanced NLP Processing**
- **Sentiment Analysis** - Detects emotions in user messages
- **Named Entity Recognition** - Extracts entities like people, places, dates
- **Pattern Matching** - Advanced regex-based intent recognition
- **Context Awareness** - Maintains conversation context
- **Intelligent Responses** - Contextual and sentiment-aware replies

### 🎨 **Beautiful UI Design**
- Modern, gradient-based color scheme
- Smooth animations and transitions
- Responsive design for all devices
- Custom scrollbars and hover effects

### 🌙 **Dark Mode Support**
- Toggle between light and dark themes
- Theme preference saved locally
- Smooth theme transitions

### ⚡ **Interactive Features**
- Real-time typing indicators
- Quick action buttons for common queries
- Keyboard shortcuts (Enter to send)
- Auto-focus on input field
- Backend connection status indicator

### � **Python Backend**
- Flask web server for API endpoints
- NLTK for sentiment analysis and tokenization
- spaCy for advanced NLP and entity extraction
- RESTful API with CORS support
- Graceful fallback mode when backend is unavailable

### �📱 **Mobile Responsive**
- Optimized for mobile devices
- Touch-friendly interface
- Adaptive layout for different screen sizes

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or download the project files**

2. **Set up the Python backend:**
   ```bash
   # Navigate to the project directory
   cd "Project 1"
   
   # Create a virtual environment (recommended)
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Start the Python backend server:**
   ```bash
   python app.py
   ```
   The server will start on `http://localhost:5000`

4. **Open the frontend:**
   - Open `index.html` in your web browser
   - Or use a simple HTTP server:
   ```bash
   # Option 1: Python server
   python -m http.server 8000
   # Then visit http://localhost:8000
   
   # Option 2: Live server in VS Code
   # Use the Live Server extension
   ```

## Usage

### Basic Conversation
1. Type your message in the input field
2. Press Enter or click the send button
3. The chatbot will respond with contextual answers
4. The bot analyzes sentiment and extracts entities for better understanding

### Quick Actions
Use the quick action buttons for common queries:
- **Hello** - Start a greeting
- **How are you?** - Ask about the bot's status
- **What can you do?** - Learn about capabilities
- **Help** - Get assistance information

### Backend Modes

**Full Mode (Backend Running):**
- Advanced NLP processing with NLTK and spaCy
- Sentiment analysis with confidence scores
- Named entity recognition
- Context-aware responses

**Fallback Mode (Backend Offline):**
- Basic pattern matching
- Limited responses
- Notifies user about backend status

## Supported Conversation Topics

The chatbot can handle various types of conversations with advanced NLP:

- **Greetings**: Hello, Hi, Hey, Good morning/evening
- **Well-being**: How are you, How do you do
- **Capabilities**: What can you do, Features, Help
- **Identity**: What's your name, Who are you
- **Time**: Current time, Date today
- **Gratitude**: Thank you, Thanks, Appreciate
- **Farewell**: Goodbye, Bye, See you
- **Sentiment-based**: Responds to positive/negative emotions

## File Structure

```
Project 1/
├── index.html          # Frontend HTML structure
├── styles.css          # CSS styling and themes
├── script.js           # Frontend JavaScript with API integration
├── app.py              # Python Flask backend
├── requirements.txt    # Python dependencies
└── README.md           # This documentation
```

## Technical Details

### Backend Technologies
- **Flask**: Web framework for API server
- **NLTK**: Natural Language Toolkit for sentiment analysis
- **spaCy**: Advanced NLP library for entity recognition
- **Flask-CORS**: Cross-origin resource sharing support

### Frontend Technologies
- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with animations
- **Vanilla JavaScript**: No framework dependencies
- **Font Awesome**: Icon library
- **Fetch API**: For backend communication

### API Endpoints

**POST /chat**
```json
Request: {"message": "Hello, how are you?"}
Response: {
    "response": "I'm doing great, thank you for asking!",
    "sentiment": "positive",
    "sentiment_scores": {"neg": 0.0, "neu": 0.5, "pos": 0.5, "compound": 0.8},
    "entities": [],
    "confidence": 0.9
}
```

**GET /health**
```json
Response: {"status": "healthy", "timestamp": "2024-01-01T12:00:00"}
```

## Customization

### Adding New Responses
Edit the `initialize_responses()` method in `app.py`:

```python
new_category: {
    'patterns': [r'\b(pattern1|pattern2)\b'],
    'responses': ['Response 1', 'Response 2']
}
```

### Modifying Colors
Update the CSS variables in `styles.css`:

```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
}
```

### Adding New NLP Features
Extend the `AdvancedNLPChatbot` class in `app.py`:

```python
def custom_nlp_feature(self, text):
    # Your custom NLP processing
    return processed_result
```

## Development

### Running in Development Mode
```bash
# Backend (with debug mode)
python app.py

# Frontend (with live reload)
python -m http.server 8000
```

### Testing the Backend
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Troubleshooting

### Common Issues

**Backend not starting:**
- Check Python version (3.8+ required)
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

**spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

**CORS errors:**
- Ensure Flask-CORS is installed
- Check that backend is running on localhost:5000

**Frontend not connecting to backend:**
- Verify backend server is running
- Check browser console for errors
- Ensure no firewall blocking localhost:5000

**NLTK data missing:**
- The app automatically downloads required NLTK data
- If issues persist, manually download:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
```

### Performance Tips

- Use virtual environment to isolate dependencies
- Restart backend server after code changes
- Clear browser cache if UI issues occur
- Monitor console for JavaScript errors

## Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## License

This project is open source and available under the MIT License.

---

Enjoy chatting with your advanced NLP-powered assistant! 🚀🐍
