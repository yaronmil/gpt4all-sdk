import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from gpt4all import GPT4All
from flask_cors import CORS
from rabbitmq import RabbitMQ
import json
import time


mock={
    'riskScore':115550,
    'riskAreas':[
        {
        "riskArea": "securityControls",
        "riskScore": 1,
        "severityId": 115548,
        "reason": "The system should have appropriate security controls in place to protect sensitive data and prevent unauthorized access. This includes implementing authentication, authorization, auditing, data validation, cryptography, error and exception handling, secure communications, secure storage, secure configuration and deployment, file handling, session management, and other relevant security measures."
        },
        {
        "riskArea": "sensitiveData",
        "riskScore": 1,
        "severityId": 115548,
        "reason": "The system should protect sensitive data such as credit card information by implementing appropriate encryption and access controls. This includes encrypting data at rest and in transit, limiting access to authorized personnel only, and regularly monitoring for any suspicious activity."
        },
        {
        "riskArea": "financialTransaction",
        "riskScore": 1,
        "severityId": 115548,
        "reason": "The system should ensure the security of financial transactions by implementing appropriate encryption and access controls. This includes encrypting data at rest and in transit, limiting access to authorized personnel only, and regularly monitoring for any suspicious activity."
        },
        {
        "riskArea": "3rdParty",
        "riskScore": 1,
        "severityId": 115548,
        "reason": "The system should ensure the security of third-party components or libraries used in application development by implementing appropriate encryption and access controls. This includes encrypting data at rest and in transit, limiting access to authorized personnel only, and regularly monitoring for any suspicious activity."
        },
        {
        "riskArea": "permissions",
        "riskScore": 1,
        "severityId": 115548,
        "reason": "The system should ensure that appropriate permissions are assigned to users based on their roles and responsibilities. This includes limiting access to sensitive data and functions only to those who need it for their job."
        },
        {
        "riskArea": "encryption",
        "riskScore": 1,
        "severityId": 115548,
        "reason": "The system should implement appropriate encryption measures to protect sensitive data at rest and in transit. This includes using strong encryption algorithms and regularly updating encryption keys."
        }
]
}
def callback(ch, method, properties, body):
    prompts=json.loads(body)

    #retVal=consultAi(prompts)
    retVal=mock
    newMessage={'taskId':prompts.get('taskId'),'response':retVal}
    time.sleep(30)
    return publish_message(newMessage)
def publish_message(msg):
    try:
        rabbitmq = RabbitMQ()
        rabbitmq.publish(queue_name='riskAssessmentAnalyzeComplete', message=json.dumps(msg))
        print("Test message published successfully.")
    except Exception as e:
        print(f"Failed to publish test message: {e}")
    
def main():
    try:
        rabbitmq = RabbitMQ()
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
        data = request.get_json()
        response=consultAi(data)
        if not response:
            return jsonify({"error": "The 'prompt' field is required"}), 400
       
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def consultAi(data):
    max_tokens = int(os.environ.get('MAX_TOKENS',8000))
    prompt = data.get('prompt')
    system_prompt = data.get('system_prompt')
    if not prompt:
       return None
    
    if system_prompt:
            with model.chat_session(system_prompt=system_prompt) as session:
                response = session.generate(prompt, max_tokens=max_tokens)
    else:
            with model.chat_session() as session:
                response = session.generate(prompt, max_tokens=max_tokens)
              
    return response

if __name__ == '__main__':
    main()
    # publish_message({'yar':'1'})
    # publish_message({'yar':'2'})
    port = int(os.environ.get('PORT',8000))
    app.run(host='0.0.0.0', port= port,debug=False)

# with model.chat_session():
#     print(model.generate("How can I run LLMs efficiently on my laptop?", max_tokens=1024))
