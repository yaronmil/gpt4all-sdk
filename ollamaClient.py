from ollama import chat
from ollama import ChatResponse
import os
import time

import ollama
from llmRunnerInterface import LlmRunnerInterface
from risk_assessment_mock_data import risk_assessmnet_mock_rsponse
risk_assessment_mock_response= [123643, 123644, 123645]
class OllamaClient(LlmRunnerInterface):
     def __init__(self):
          self.model_name=os.environ.get('OLLAMA_MODEL_NAME')
          

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
                response:ChatResponse=ollama.generate(model=self.model_name, prompt=prompt, system=system_prompt,options={'temperature':0.3   })
                # response: ChatResponse = chat(model=self.model_name, messages=[
                #     {
                #         'role': 'user',
                #         'content': 'Why is the sky blue?',
                #     },
        # ])
       
                
        return response.response

          