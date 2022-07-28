# gpsd_influx2
Based on https://github.com/mzac/gpsd-influx

Updated to use the influxdb v2 API, also added satellites visibility and tracked counts to the log output.


Required gpsd libraries and influxdb-client
```
pip install influxdb-client
```

It loads the configuration from config.ini, the format is standard. It needs to be placed in the same directory as the python script, e.g. /opt/gpsd_influx2/config.ini

```
[influx2]
url=http://localhost:8086
org=my-org
token=my-token
timeout=6000
verify_ssl=False
```

/etc/systemd/system/gpsd_influx2.service
```
[Unit]
Description=GPSD to Influx
After=syslog.target

[Service]
WorkingDirectory=/opt/gpsd_influx2/
ExecStart=/usr/bin/python3 /opt/gpsd_influx2/gpsd_influx2.py
KillMode=process
Restart=on-failure
User=<user>

[Install]
WantedBy=multi-user.target
```

Then the usual:
```
sudo systemctl daemon-reload
sudo systemctl enable gpsd_influx2
sudo systemctl start gpsd_influx2
```

Errors will be logged, if nothing goes wrong no outputs will be generated:
```
journalctl -fu gpsd_influx2.service
```
