import network, time, machine, onewire, ds18x20, secrets
from umqtt.simple import MQTTClient

# Set up the onewire interface
ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
print('Found DS devices: ', roms)

# Connect to wireless network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.LAN_SSID, secrets.LAN_PASSWORD)

while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

# Set up MQTT client
mqtt_host = secrets.MQTT_HOST
mqtt_username = secrets.MQTT_USERNAME
mqtt_password = secrets.MQTT_PASSWORD
mqtt_publish_topic = secrets.MQTT_TOPIC
mqtt_client_id = secrets.MQTT_CLIENTID

mqtt_client = MQTTClient(
    client_id = mqtt_client_id,
    server = mqtt_host,
    user = mqtt_username,
    password = mqtt_password)

# Loop to check temperature at regular intervals and publish to configured MQTT topic
while True:
    try:
      mqtt_client.connect()
      ds_sensor.convert_temp()
      time.sleep_ms(750)
      for rom in roms:
        mqtt_client.publish(mqtt_publish_topic, str(ds_sensor.read_temp(rom)))
    except Exception as e:
         print(f'Failed to publist message: {e}')
    
    finally:
        mqtt_client.disconnect()
        time.sleep(300)
