from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Replace with your actual OpenAI API key
openai.api_key = 'your_openai_api_key_here'

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data['message']
    conversation_history = data['conversation_history']

    # Add system message to guide the AI's behavior
    conversation_history.insert(0, {
        "role": "system",
        "content": "You are an AI assistant helping users fill out a form. Ask questions one at a time to gather information for the form fields: name, email, age, project name, project description, project use case, project outcomes, and project execution plan. After each response, provide the information in a format that can be easily parsed, like 'Name: John Doe'."
    })

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        ai_response = response.choices[0].message['content']
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    form_data = data['form_data']

    # Process the form data as needed
    # For example, save it to a database or send it via email

    return jsonify({"message": "Form data submitted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
