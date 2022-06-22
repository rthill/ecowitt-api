from datetime import datetime

from influxdb import InfluxDBClient


def convert_mph_kmh(val):
    """Convert mp/h into km/h"""

    return val * 0.6214


def convert_f_c(val):
    """Convert degree F to degree C"""

    return (val - 32) * 5 / 9


def convert_dt_ts(val):
    """Convert datetime to timestamp"""

    dt = datetime.strptime(val, "%Y-%m-%d %H:%M:%S")

    return dt.strftime("%s")


def send_to_influxdb(fields, host="127.0.0.1", port=8086, db="weather"):
    req = {"measurement": "weather", "tags": {}, "fields": {}}

    for k, v in fields.items():
        if v is not None:
            req["fields"][k] = v

    reqs = []
    reqs.append(req)

    try:
        client = InfluxDBClient(host=host, port=port, database=db)
        client.write_points(reqs)
    except BaseException:
        pass
