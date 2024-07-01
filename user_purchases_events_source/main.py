from quixstreams import Application  # import the Quix Streams modules for interacting with Kafka:
# (see https://quix.io/docs/quix-streams/v2-0-latest/api-reference/quixstreams.html for more details)

# import additional modules as needed
import random
import os
import json
import csv
import random
from datetime import datetime, timedelta
import time

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="data_source", auto_create_topics=True)  # create an Application

# define the topic using the "output" environment variable
topic_name = os.environ["output"]
topic = app.topic(topic_name)


def main():
    # create a pre-configured Producer object.
    with app.get_producer() as producer:
        while True:
            user_id = random.randint(1001, 1020)
            purchase_amount = round(random.uniform(10.0, 500.0), 2)

            timestamp = int(time.time() * 1000)
            
            payload = {
                "user_id": user_id,
                "timestamp": timestamp,
                "purchase_amount": purchase_amount
            }


            # publish the data to the topic
            producer.produce(
                topic=topic.name,
                key=str(user_id).encode('utf-8'),
                value=json.dumps(payload),
                timestamp=timestamp
            )

            print(payload)
            
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting.")



