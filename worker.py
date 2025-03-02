import pika
import json
import time
import os

from gpt4allClient  import Gpt4AllClient
import llmRunnerInterface

class Worker:
    def __init__(self,aiModel:llmRunnerInterface):
        self.aiModel=aiModel
        self.user = os.getenv('RABBITMQ_USER', 'user')
        self.password = os.getenv('RABBITMQ_PASS', 'pass')
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT'))
        self.connection = None
        self.channel = None
        while True:
            try:
                print("trying to connect to rabbit")
                self.connect()
            except:
                print("connecting to rabbit failed")
                time.sleep(5)
                continue

    def risk_assessment_cb(self,ch, method, properties, body):
        prompts=json.loads(body)
        taskId=prompts.get('taskId')
        print(f"start analyzing risk_assessment {taskId}")
        retVal=self.aiModel.consultAi(prompts,True)
        newMessage={'taskId':taskId,'response':retVal}
        try:
            self.publish("risk_assessment_ai_response",method,newMessage)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Failed to publish {taskId} {e}")

    def sec_req_cb(self,ch, method, properties, body):
        prompts=json.loads(body)
        taskId=prompts.get('taskId')
        print(f"start analyzing sec_req {taskId}")
        retVal=self.aiModel.consultAi(prompts,False)
        newMessage={'taskId':taskId,'response':retVal}
        try:
            self.publish("define_security_requirements_ai_response",method,newMessage)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Failed to publish {taskId} {e}")

   

    def connect(self):
        """Establish connection to RabbitMQ and declare the queue."""

        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials,  client_properties={
        'connection_name': 'gpt4all',
        'custom_property': 'value123'
        } )

 
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="risk_assessment",durable=True)
        self.channel.queue_declare(queue="define_security_requirements",durable=True)
        print("Connected to RabbitMQ. Listening on queue: risk_assessment,define_seq_req")
        self.channel.basic_consume(queue='risk_assessment', on_message_callback=self.risk_assessment_cb)
        self.channel.basic_consume(queue='define_security_requirements', on_message_callback=self.sec_req_cb)
        self.channel.start_consuming()
        print("Waiting for RPC requests...")
    

    def on_message(self, ch, method, properties, body):
        """Handle incoming messages."""
        request = json.loads(body)
        if not request.get("isReply"):  # Check if it's a request message
            print(f"Received request: {request}")

            # Perform the long-running task
            response = self.long_running_task(request)

            # Send the response back to the same queue
            ch.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id,  # Match correlation ID
                ),
                body=json.dumps({"isReply": True, "data": response}),
            )

        # Acknowledge the request message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def stop(self):
        """Clean up resources."""
        if self.connection:
            self.connection.close()
            print("RabbitMQ connection closed.")

    def publish(self, queue_name,method, message):
        if not self.channel:
            raise Exception("Connection is not established.")
        taskId=message.get('taskId')
        print(f"analyzing complete {taskId}")
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=json.dumps(message),
                                   )
       
        print(f"sent message to queue {queue_name}: {message}")
            