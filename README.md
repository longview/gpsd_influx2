# gpsd_influx2
Based on https://github.com/mzac/gpsd-influx

Updated to use the influxdb v2 API, also added satellites visibility and tracked counts to the log output.

You can also optionally log detailed satellite information by adding -s to the command line.
Use -o to disable database writes (useful with -d)

## Grafana Dashboard
![Grafana Dashboard](/grafana.png)
![Grafana Dashboard](/grafana2.png)

The Grafana dashboard is tested on OSS version 9.0.5, it uses the [pr0ps TrackMap panel](https://grafana.com/grafana/plugins/pr0ps-trackmap-panel/) to display the position on a 2D map.

```
grafana-cli plugins install pr0ps-trackmap-panel
```

Change the 'host' variable to change what hostname the data is reported for.

## Installation
Requires gpsd libraries and influxdb-client
```
pip install influxdb-client
```
Then pull into /opt
```
cd /opt

sudo git clone https://github.com/longview/gpsd_influx2.git
```
It loads the configuration from config.ini, the format is standard. A sample file in included, edit it to add your database details & API key.

Copy gpsd_influx2.service /etc/systemd/system/ and update the User field

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

## Update
Very simple.
```
cd /opt/gpsd_influx2
sudo git pull
sudo systemctl restart gpsd_influx2
```
