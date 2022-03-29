# Fitness Processing
Gets the heart rate of all GPX files in the parent directory and calculates how long in each HR zone was trained. This data is then saved to a defined influxDB and the GPX track is moved to the archive folder.

It also imports all present weight logs from a specified folder from [Libra - Weight Manager](https://play.google.com/store/apps/details?id=net.cachapa.libra&hl=en&gl=US) and stores these into the influxDB.

The purpose is to first store the data in a save place like influx and to get some nice visualizations using [Grafana](https://grafana.com/)
