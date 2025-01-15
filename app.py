from threading import Thread
from dotenv import load_dotenv
from controller import apiServer
from gpt4all_client import gpt4AllClient
from risk_assessment_worker import RiskAssessmentWorker
load_dotenv()

aiModel=gpt4AllClient()
serverThread = Thread(target=apiServer,args=(aiModel,))
serverThread.start()
worker = RiskAssessmentWorker(aiModel=aiModel)

#if __name__ == '__main__':
