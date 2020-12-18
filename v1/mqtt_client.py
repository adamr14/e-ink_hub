import paho.mqtt.client as mqtt
import json
import os
import sys

def on_connect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe(("emma", 0))

def on_message(client, userdata, msg):
    print(msg.payload)
    os.chdir(os.path.dirname(sys.argv[0]))
    with open('./data/message.txt', 'w') as outfile:
        outfile.write(msg.payload.decode("utf-8"))
    
def main():
    os.chdir(os.path.dirname(sys.argv[0]))
    with open('./credentials/credentials.txt', 'r') as credentials_file:
        credentials = json.load(credentials_file)
    print(credentials)    
    client = mqtt.Client()
    client.username_pw_set(credentials['mqtt']['user'], password=credentials['mqtt']['pass'])
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect('driver.cloudmqtt.com', 18981, 60)
    client.loop_forever()


if __name__ == '__main__':
    main()