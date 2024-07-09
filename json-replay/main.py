from quixstreams import Application
import json
import time
import os

# import the dotenv module to load environment variables from a file
from dotenv import load_dotenv
load_dotenv(override=False)

# Create an Application.
app = Application.Quix()

# Define the topic using the "output" environment variable
topic_name = os.getenv("output", "")
if topic_name == "":
    raise ValueError("The 'output' environment variable is required. This is the output topic that data will be published to.")

topic = app.topic(topic_name)

with app.get_producer() as producer:
    with open(os.environ["file"], 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Remove newline characters from the message
            message = json.loads(line.strip())
            
            if message is None:
                continue
            
            if "after" in message and message["after"] is not None:
                message_key = message["after"]["user_idn"]
            elif "before" in message and message["before"] is not None:
                message_key = message["before"]["user_idn"]
            else:
                message_key = None
                            
            
            # Publish message to Kafka
            producer.produce(topic.name, json.dumps(message), message_key)

            print(message)
            time.sleep(1)

    producer.flush(30)  # Wait for all messages to be delivered
    print('All messages have been flushed to the Kafka topic')