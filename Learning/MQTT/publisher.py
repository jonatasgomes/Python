import paho.mqtt.client as mqtt
import time

broker = 'broker.emqx.io'
port = 1883
topic = 'fiap/ai/demo'

client = mqtt.Client(protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker, port, 60)

for i in range(5):
    message = f'Hello MQTT {i}'
    client.publish(topic, message)
    print(f'Sent: {message}')
    time.sleep(1)
client.disconnect()
