# gpsd_influx2
Based on https://github.com/mzac/gpsd-influx


Required gpsd libraries and influxdb-client
```
pip install influxdb-client
```

It loads the configuration from config.ini, the format is standard. It needs to be placed in the same directory as the python script, e.g. /opt/gpsd-influx2/config.ini

```
[influx2]
url=http://localhost:8086
org=my-org
token=my-token
timeout=6000
verify_ssl=False
```

/etc/systemd/system/gpsd-influx2.service
```
[Unit]
Description=GPSD to Influx
After=syslog.target

[Service]
WorkingDirectory=/opt/gpsd-influx2/
ExecStart=/usr/bin/python3 /opt/gpsd-influx2/gpsd-influx2.py
KillMode=process
Restart=on-failure
User=<user>

[Install]
WantedBy=multi-user.target
```
