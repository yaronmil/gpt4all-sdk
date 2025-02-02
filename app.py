from threading import Thread
from dotenv import load_dotenv
from api_server import apiServer
from ai_client import aiClient
from worker import Worker
load_dotenv()

aiModel=aiClient()
serverThread = Thread(target=apiServer,args=(aiModel,),daemon=True)
serverThread.start()
worker = Worker(aiModel=aiModel)

#if __name__ == '__main__':
