import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from chatbot import BudgetBot


# Load environment variables from .env file (for any configuration like API keys)
load_dotenv()


app = Flask(__name__)


# Initialize the BudgetBot
budget_bot = BudgetBot()


@app.route('/')
def empty():
    return render_template("chatbot.html")


@app.route('/chat/message', methods=['POST'])
def chat():
    """Route to handle chat interactions."""
    data = request.get_json()


    # Ensure data is valid
    if not data or 'user_id' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid input, please provide user_id and message.'}), 400


    user_id = data['user_id']
    text = data['message']
    context = data.get('context', None)
   
    # Process the message through BudgetBot
    response = budget_bot.process_message(text, user_id, context)
   
    return jsonify({'response': response}), 200


@app.route('/analyze_spending', methods=['POST'])
def analyze_spending():
    """Route to analyze user spending over a given timeframe."""
    data = request.get_json()




    if not data or 'user_id' not in data:
        return jsonify({'error': 'Invalid input, please provide user_id.'}), 400




    user_id = data['user_id']
    timeframe = data.get('timeframe', 'month')  # Default timeframe is 'month'
   
    # Get spending analysis from the bot
    analysis = budget_bot.analyze_spending(user_id, timeframe)
   
    return jsonify({'analysis': analysis}), 200




if __name__ == "__main__":
    app.run(debug=True)



