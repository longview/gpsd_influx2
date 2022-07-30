# gpsd_influx2
Based on https://github.com/mzac/gpsd-influx

Updated to use the influxdb v2 API, also added satellites visibility and tracked counts to the log output.

You can also optionally log detailed satellite information by adding -s to the command line.
Use -o to disable database writes.

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

Create to gpsd_influx2.service /etc/systemd/system/ and update the User field

Then the usual:
```
sudo systemctl daemon-reload
sudo systemctl enable gpsd_influx2
sudo systemctl start gpsd_influx2
```

The default service script is linked to gpsd.service, and will restart if gpsd.service is restarted. This is to work around an issue where the gpsd client hangs if the service is restarted.

Errors will be logged, if nothing goes wrong no outputs will be generated:
```
journalctl -fu gpsd_influx2.service
```
