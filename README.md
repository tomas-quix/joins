# Example of Join Operation with QuixStreams

This project demonstrates a workaround for performing join operations with the QuixStreams library before the join operator is introduced. It is intended for developers who need to implement join functionality in their data pipelines now.

## Project Overview

### Description
This pipeline example shows how to join user activity events with purchase events using the QuixStreams library. The join operation is performed through a series of services that read from and write to different topics, effectively simulating a join operation.

## Installation and Setup

### Dependencies
- Python 3.8+
- QuixCLI (https://github.com/quixio/quix-cli)

### Installation Steps
1. Clone this repository.
2. Ensure you have Python 3.8+ installed.

## Usage

### How to Run the Pipeline
To run the pipeline, you need to deploy the services defined in the `quix.yaml` file. Each service represents a part of the pipeline, from generating events to performing the join operation.

To run pipeline using docker compose run QuixCLI command:
```
quix pipeline up
```

1. **Deploy Services**: Deploy each service as described in the `quix.yaml` file.
    - `user_activity_events_source`: Generates user activity events.
    - `user_purchases_events_source`: Generates purchase events.
    - `join_user_purchases`: Reads purchase events and writes to a pre-join topic.
    - `join_user_activities`: Reads user activity events and writes to a pre-join topic.
    - `join`: Joins data from the pre-join topic and writes to the joined topic performing time-based join.