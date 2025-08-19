import paho.mqtt.client as mqtt

broker = 'broker.emqx.io'
port = 1883
topic = 'fiap/ai/demo'

def on_message(client, userdata, message):
    print(f'Received: {message.payload.decode()} on topic {message.topic}')

client = mqtt.Client(protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(broker, port, 60)
client.subscribe(topic)

print('Waiting for messages...')
client.loop_forever()
