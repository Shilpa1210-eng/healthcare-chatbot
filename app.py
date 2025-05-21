from flask import Flask, render_template, request, jsonify
from chat_bot import get_bot_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message')
    if user_message:
        bot_reply = get_bot_response(user_message)
        return jsonify({'reply': bot_reply})
    else:
        return jsonify({'reply': "Sorry, I didn't understand that."})

if __name__ == '__main__':
    app.run(debug=True)
