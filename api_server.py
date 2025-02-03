import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from ai_client import aiClient


class apiServer:
    app = Flask(__name__)
    CORS(app)
    def __init__(self,aiModel:aiClient):
        self.aiModel=aiModel
        port = int(os.environ.get('PORT',8000))
        self.app.add_url_rule( '/query','risk_assessment', view_func=self.risk_assessment_model,methods=['POST'])
        self.app.run(host='0.0.0.0', port= port,debug=False)
    
    def risk_assessment_model(self ):
        try:
            data = request.get_json()
            response=self.aiModel .consultAi(data,True,True)
            if not response:
                return jsonify({"error": "The 'prompt' field is required"}), 400
        
            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500