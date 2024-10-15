import json


class Publisher:
    def __init__(self, logger, client, topic):
        self.logger = logger
        self.client = client
        self.topic = topic

    def publish(self, message: dict):
        try:
            jsonstr = json.dumps(message)
            bytedata = jsonstr.encode()
            self.client.publish(self.topic, bytedata)
        except Exception as err:
            self.logger.error(f"Failed to publish message: {str(err)}")