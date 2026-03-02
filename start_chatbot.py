import subprocess
import sys
import time
import webbrowser
import os

def start_chatbot():
    print("🚀 Starting Advanced NLP Chatbot...")
    print("=" * 50)
    
    # Start the Python backend
    print("📡 Starting Python backend server...")
    try:
        # Start the Flask app in background
        subprocess.Popen([sys.executable, "simple_app.py"], 
                       cwd=os.path.dirname(os.path.abspath(__file__)))
        print("✅ Backend server starting on http://localhost:5000")
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open the frontend
        print("🌐 Opening frontend in browser...")
        webbrowser.open('file://' + os.path.abspath('index.html'))
        
        print("=" * 50)
        print("🎉 Chatbot is ready!")
        print("📝 Features:")
        print("   • Advanced NLP with sentiment analysis")
        print("   • Beautiful UI with dark mode")
        print("   • Real-time sentiment indicators")
        print("   • Intelligent responses")
        print("=" * 50)
        print("💡 Keep this terminal open to maintain the backend connection")
        print("🛑 Press Ctrl+C to stop the server")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down chatbot server...")
            
    except Exception as e:
        print(f"❌ Error starting chatbot: {e}")
        print("💡 Make sure you have all dependencies installed:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    start_chatbot()
