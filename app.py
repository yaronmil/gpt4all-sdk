import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from gpt4all import GPT4All
from flask_cors import CORS
from rabbitmq import RabbitMQ
import json
 

def callback(ch, method, properties, body):
    print(f"Received message: {body}")
def publish_message(msg):
    try:
        rabbitmq = RabbitMQ();
        rabbitmq.publish(queue_name='riskAssessmentAnalyzeComplete', message=json.dumps(msg))
        print("Test message published successfully.")
    except Exception as e:
        print(f"Failed to publish test message: {e}")
    
def main():
    try:
        rabbitmq = RabbitMQ();
        rabbitmq.consume(queue_name='riskAssessmentAnalyze', callback=callback)
    except Exception as e:
        print(f"Failed to establish connection to RabbitMQ: {e}")

load_dotenv()
app = Flask(__name__)
CORS(app)
MODEL=os.environ.get('MODEL_NAME')
model = GPT4All(MODEL, device = "cpu") # downloads / loads a 4.66GB LLM

# Define your system prompt

@app.route('/query', methods=['POST'])
def risk_assessment_model():
    try:
        max_tokens = int(os.environ.get('MAX_TOKENS',8000))
        # Parse the JSON payload from the POST request
        data = request.get_json()

        # Validate the 'prompt' field (mandatory)
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "The 'prompt' field is required"}), 400

        # Get the 'system_prompt' field (optional) 
        system_prompt = data.get("system_prompt", None)

        # Start a chat session with or without a system prompt
        if system_prompt:
            with model.chat_session(system_prompt=system_prompt) as session:
                response = session.generate(prompt, max_tokens=max_tokens)
        else:
            with model.chat_session() as session:
                response = session.generate(prompt, max_tokens=max_tokens)

        # Return the generated response as JSON
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    main()
    # publish_message({'yar':'1'})
    # publish_message({'yar':'2'})
    port = int(os.environ.get('PORT',8000))
    app.run(host='0.0.0.0', port= port,debug=False)

# with model.chat_session():
#     print(model.generate("How can I run LLMs efficiently on my laptop?", max_tokens=1024))
