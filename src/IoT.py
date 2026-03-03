import paho.mqtt.client as mqtt
import json
import time
import random
import ssl
import os
from datetime import datetime
from obs import ObsClient

HOST = "80b28ec17e.st1.iotda-device.ap-southeast-3.myhuaweicloud.com"
PORT = 8883
DEVICE_ID = "6999704beaf74870a81d32a7_soilmate_sensor_01_0_0_2026022215"
USERNAME = "6999704beaf74870a81d32a7_soilmate_sensor_01"
PASSWORD = "b6adb571fbf2ef27254dcba90c74d72037094b7ca8f4d8450b1894596f4bedc9"
TOPIC = f"$oc/devices/{DEVICE_ID}/sys/properties/report"

OBS_AK = "HPUAR9BHMQVOKBCR9R99"
OBS_SK = "QJWRU0w7Pi0Wy0L6QKpJfZUiDJfsHwYrW9viy7rQ"
OBS_ENDPOINT = "obs.ap-southeast-3.myhuaweicloud.com"
OBS_BUCKET_NAME = "soilmate-data"
OBS_FOLDER_NAME = "sensor_values"
LOCAL_CSV = "sensor_data.csv"
LATEST_JSON = "latest_sensor_data.json"

obs_client = ObsClient(access_key_id=OBS_AK, secret_access_key=OBS_SK, server=OBS_ENDPOINT)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected Successfully to Huawei Cloud IoTDA")
    else:
        print(f"Connection Failed: {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=DEVICE_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.on_connect = on_connect

print("Connecting to Huawei Cloud IoTDA...")
client.connect(HOST, PORT, 60)
client.loop_start()

try:
    while True:
        temp = round(random.uniform(15.0, 35.0), 2)
        hum = round(random.uniform(30.0, 80.0), 2)
        rain = round(random.uniform(0.0, 50.0), 2)
        ph_val = round(random.uniform(5.5, 8.5), 2) 
        n_val = random.randint(10, 100)
        p_val = random.randint(10, 100)
        k_val = random.randint(10, 100)
        now = datetime.now()

        print("-" * 30)
        print(f"N: {n_val} | P: {p_val} | K: {k_val} | pH: {ph_val}")

        live_data = {
            "N": n_val, "P": p_val, "K": k_val, 
            "pH": ph_val, "Temperature": temp, "Humidity": hum,
            "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(LATEST_JSON, "w") as jf:
            json.dump(live_data, jf)

        payload = {
            "services": [{
                "service_id": "AgriCultureData",
                "properties": {
                    "Temperature": temp, "Humidity": hum, "Precipitation": rain,
                    "pH": ph_val, "N": n_val, "P": p_val, "K": k_val,
                    "Latitude": 37.0000, "Longitude": 35.3213,
                    "Status": "Active"
                }
            }]
        }
        client.publish(TOPIC, json.dumps(payload))
        
        file_exists = os.path.isfile(LOCAL_CSV)
        with open(LOCAL_CSV, "a") as f:
            if not file_exists:
                f.write("Temperature,Humidity,Precipitation,pH,N,P,K,Timestamp\n")
            f.write(f"{temp},{hum},{rain},{ph_val},{n_val},{p_val},{k_val},{now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        object_key = f"{OBS_FOLDER_NAME}/sensor_data_{now.strftime('%Y-%m-%d')}.csv"
        resp = obs_client.putFile(OBS_BUCKET_NAME, object_key, LOCAL_CSV)
        
        if resp.status < 300:
            print(f" -> OBS Backup Success")
        else:
            print(f" -> OBS Error: {resp.errorMessage}")
            
        time.sleep(10)

except KeyboardInterrupt:
    print("\nStopped by User")
    client.loop_stop()
    client.disconnect()
    obs_client.close()