import os

from flask import Flask, jsonify, request
from flask_mqtt import Mqtt

from utils import convert_dt_ts, convert_f_c, convert_mph_kmh

DEBUG = os.environ.get("DEBUG", False)
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "ecowitt")

app = Flask("ecowitt-api")
app.config["MQTT_BROKER_URL"] = os.environ.get("MQTT_BROKER_URL", "localhost")
app.config["MQTT_BROKER_PORT"] = os.environ.get("MQTT_BROKER_PORT", 1883)
app.config["MQTT_USERNAME"] = os.environ.get("MQTT_USERNAME", "")
app.config["MQTT_PASSWORD"] = os.environ.get("MQTT_PASSWORD", "")
app.config["MQTT_KEEPALIVE"] = os.environ.get("MQTT_KEEPALIVE", 20)
app.config["MQTT_TLS_ENABLED"] = os.environ.get("MQTT_TLS_ENABLED", False)

mqtt = Mqtt()

ignored_params = ["PASSKEY", "stationtype", "model"]
f_to_c = ["tempinf", "tempf"]
mph_to_kmh = ["windspeedmph", "windgustmph", "maxdailygust"]
not_float = ["runtime", "dateutc", "freq"]


@app.route("/api/v1", methods=["POST"])
def api():
    if request.method == "POST":
        data = request.form

        for k, v in data.items():
            if k not in ignored_params:
                if k not in not_float:
                    v = float(v)

                if k in f_to_c:
                    if k.endswith("f"):
                        k = k.replace("f", "c")
                    v = round(convert_f_c(v), 2)
                elif k in mph_to_kmh:
                    if k.endswith("mph"):
                        k = k.replace("mph", "kmh")
                    v = round(convert_mph_kmh(v), 3)
                elif k == "dateutc":
                    k = "time"
                    v = convert_dt_ts(v)

                mqtt.publish(f"{MQTT_TOPIC}/{k}", v)

    return jsonify("OK")


if __name__ == "__main__" and DEBUG:
    app.run(host="0.0.0.0", port=8180, debug=True)
