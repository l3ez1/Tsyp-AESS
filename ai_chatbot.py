import openai
from flask import Flask, request, jsonify
import os

# Ensure the API key is loaded from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Root route for testing the server
@app.route("/", methods=["GET"])
def home():
    return "AI Chatbot API is running. Use the /chat endpoint for queries."

# Chatbot endpoint
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_query = data.get("query", "")
        dashboard_data = data.get("dashboard_data", {})

        # Validate inputs
        if not user_query:
            return jsonify({"error": "Missing 'query' field in the request."}), 400

        # Prepare dynamic context
        context = (
            f"You are assisting with a land cover monitoring dashboard. "
            f"The user is analyzing land cover data for {dashboard_data.get('land_cover', 'unknown land cover')} "
            f"from {dashboard_data.get('start_year', 'unknown year')} to {dashboard_data.get('end_year', 'unknown year')}.\n\n"
            f"User Query: {user_query}"
        )

        # Generate response using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant for land monitoring."},
                {"role": "user", "content": context},
            ],
            max_tokens=200,
            temperature=0.7,
        )

        ai_response = response['choices'][0]['message']['content']
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(debug=True, port=5000)
