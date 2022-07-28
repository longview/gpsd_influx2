# gpsd_influx2
Based on https://github.com/mzac/gpsd-influx

Updated to use the influxdb v2 API, also added satellites visibility and tracked counts to the log output.

You can also optionally log detailed satellite information by adding -s to the command line.

Required gpsd libraries and influxdb-client
```
pip install influxdb-client
```
Then pull into /opt
```
cd /opt

sudo git pull https://github.com/longview/gpsd_influx2.git
```
It loads the configuration from config.ini, the format is standard. A sample file in included, edit it to add your database details & API key.

Create /etc/systemd/system/gpsd_influx2.service
```
[Unit]
Description=GPSD to Influx
After=syslog.target

[Service]
WorkingDirectory=/opt/gpsd_influx2/
ExecStart=/usr/bin/python3 /opt/gpsd_influx2/gpsd_influx2.py -s
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
