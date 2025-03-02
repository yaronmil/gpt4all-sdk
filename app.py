from threading import Thread
from dotenv import load_dotenv
from api_server import apiServer
from gpt4allClient import Gpt4AllClient
from ollamaClient import OllamaClient
from worker import Worker
load_dotenv()

# aiModel=Gpt4AllClient()
aiModel=OllamaClient()
serverThread = Thread(target=apiServer,args=(aiModel,),daemon=True)
serverThread.start()
worker = Worker(aiModel=aiModel)

#if __name__ == '__main__':
