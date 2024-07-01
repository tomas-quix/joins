import os
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta

app = Application(consumer_group="join-v1.4", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

sdf = sdf.group_by(lambda row: str(row["user_id"]), "user_id")

def reduce_window(state: dict, row: dict):
    
    if "activity_type" in row:
        return{
            **row,
            "purchases_sum": state["purchases_sum"] 
        }
    
    return {
        "purchases_sum": state["purchases_sum"] + row["purchase_amount"]
    }
    
def init_window(row: dict):
    
    if "purchases_sum" in row:
        return {
            "purchases_sum": row["purchases_sum"]
        }
    
    return {
        **row,
        "purchases_sum": 0
    }

sdf = sdf.hopping_window(timedelta(minutes=10), timedelta(minutes=1), 5000) \
    .reduce(reduce_window, init_window) \
    .current()


sdf = sdf.apply(lambda row: row["value"])

sdf = sdf[sdf.contains("activity_type")]

sdf = sdf.set_timestamp(lambda row, *_: row["timestamp"])

sdf = sdf.update(lambda row: print(row))

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)