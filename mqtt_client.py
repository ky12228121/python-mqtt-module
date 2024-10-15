import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, logger, broker_address, port=1883, keepalive=60):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.port = port
        self.keepalive = keepalive
        self.logger = logger

    def on_connect(self, client, userdata, flags, rc):
        if rc == mqtt.CONNACK_ACCEPTED:
            self.logger.info("Connected to MQTT broker")
        else:
            self.logger.error(f"Failed to connect to MQTT broker. Error code: {rc}")

    def on_disconnect(self, client, userdata, rc):
        if rc != mqtt.CONNACK_ACCEPTED:
            self.logger.warning("Unexpected disconnection occurred. Attempting to reconnect.")
            try:
                self.client.reconnect()
                self.logger.info("Successfully reconnected.")
            except Exception as e:
                self.logger.error(f"Failed to reconnect: {str(e)}")

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(self.broker_address, self.port, self.keepalive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic: str, payload: bytes, qos=0, retain=False):
        result = self.client.publish(topic, payload, qos, retain)
        return result.rc
