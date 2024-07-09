import os
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta

app = Application(consumer_group="join-v1.9", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

#sdf = sdf.group_by(lambda row: (row["user_id"]), "user_id")

def reduce_window(state: dict, row: dict):
    state = {**state, **row["after"]}
    return state
    
    
def init_window(row: dict):
    return row["after"]

sdf = sdf[sdf.contains("after") & sdf["after"].notnull()]


sdf = sdf.hopping_window(timedelta(hours=1), timedelta(minutes=1), timedelta(hours=1)) \
    .reduce(reduce_window, init_window) \
    .current()
    
sdf = sdf.apply(lambda row: row["value"])
    



# Filter items that are already joined.
sdf = sdf[sdf.contains("enc_idn") & sdf.contains("mbr_first_name")]

sdf = sdf.update(lambda row: print(row))

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)