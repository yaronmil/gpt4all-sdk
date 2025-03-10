from gpt4all import GPT4All
import os
import time
from llmRunnerInterface import LlmRunnerInterface
from risk_assessment_mock_data import risk_assessmnet_mock_rsponse
risk_assessment_mock_response= [123643, 123644, 123645]
class Gpt4AllClient(LlmRunnerInterface):
     def __init__(self):
          model_name=os.environ.get('MODEL_NAME')
          self.model = GPT4All(model_name, device = "cpu")

     def consultAi(self,data,isRiskAssessment,ignoreMockConfig=False):
        if(not ignoreMockConfig):
            if os.environ.get('GPT_MOCK')=='1':
                delay=int(os.environ.get('AI_DELAY_SEC',1)) 
                time.sleep(delay)
                if(isRiskAssessment==True):
                 return risk_assessmnet_mock_rsponse
                else:
                     return risk_assessment_mock_response
        
        max_tokens = int(os.environ.get('MAX_TOKENS',8000))
        prompt = data.get('prompt')
        system_prompt = data.get('system_prompt')
        if not prompt:
         return None
        
        if system_prompt:
                with self.model.chat_session(system_prompt=system_prompt) as session:
                    response = session.generate(prompt, max_tokens=max_tokens)
        else:
                with self.model.chat_session() as session:
                    response = session.generate(prompt, max_tokens=max_tokens)
                
        return response

          