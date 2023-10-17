import paho.mqtt.client as mqtt

# Define the MQTT broker address and port
broker_address = "localhost"
port = 1883

# Define the MQTT topic you want to subscribe to
topic = "test_topic"

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

# Callback when a message is received from the subscribed topic
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

# Create an MQTT client
client = mqtt.Client()

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, port, 60)

# Start the MQTT client loop to listen for messages
client.loop_forever()
