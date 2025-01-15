from threading import Thread
from dotenv import load_dotenv
from api_server import apiServer
from ai_client import aiClient
from risk_assessment_worker import RiskAssessmentWorker
load_dotenv()

aiModel=aiClient()
serverThread = Thread(target=apiServer,args=(aiModel,),daemon=True)
serverThread.start()
worker = RiskAssessmentWorker(aiModel=aiModel)

#if __name__ == '__main__':
