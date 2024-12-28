# app/routes/api.py

from flask import Blueprint, jsonify, request
import google.generativeai as genai
import os

# Create the Blueprint for the API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Configure the Google Generative AI API (using .env file for security)
genai_api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if genai_api_key:
    genai.configure(api_key=genai_api_key)
else:
    raise ValueError("GOOGLE_GENAI_API_KEY environment variable not set!")

# AI Model Configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 256,
}

# Route: Generate AI-driven content for counseling
@api_bp.route('/generate_counseling', methods=['POST'])
def generate_counseling_response():
    """
    Endpoint to generate AI responses for counseling.
    Expects JSON payload: { "prompt": "Your counseling query here." }
    """
    data = request.get_json()
    prompt = data.get('prompt', '').strip()

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        # Initialize AI model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config
        )

        # Generate response from AI
        response = model.generate(input=prompt)
        return jsonify({'response': response.text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route: Health Check
@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint to check API health.
    """
    return jsonify({'status': 'API is running'}), 200


# Route: AI Suggestions for Habits or Schedules
@api_bp.route('/generate_suggestions', methods=['POST'])
def generate_suggestions():
    """
    Endpoint to generate AI suggestions for habits or schedules.
    Expects JSON payload: { "query": "What are some productive habits?" }
    """
    data = request.get_json()
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        # Initialize AI model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config
        )

        # Generate response from AI
        response = model.generate(input=query)
        return jsonify({'suggestions': response.text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
