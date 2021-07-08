# monitoring

### 1) fetch the image and build it

https://github.com/XN137/docker-graphite-grafana

```
git clone https://github.com/XN137/docker-graphite-grafana
cd docker-graphite-grafana
docker build -t 2021-07-05-graphite-grafana .
```

### 2) run the image mounting volumens for persistent data storage in /var/lib/gmonitor

```
docker run -v /var/lib/gmonitor/graphite/whisper:/var/lib/graphite/storage/whisper \
           -v /var/lib/gmonitor/graphite/conf:/var/lib/graphite/conf \
           -v /var/lib/gmonitor/grafana/data:/usr/share/grafana/data \
           -p 2003:2003 \
           -p 2004:2004 \
           -p 3005:3000 \
           -p 8080:80 \
           -d 2021-07-05-graphite-grafana

```

### 3) navigate to webserver admin:admin

- grafana
http://localhost:3005/login/

- graphite
http://localhost:8080/

### 4) set up cron job to run the python script to log the information into the data base
```
crontab -e
```


```
*/2 * * * * /home/lardilap/Projects/Shelf_Monitoring/monitoring/scripts/kit_scrape.py >> /home/lardilap/Projects/Shelf_Monitoring/monitoring/scripts/log/`date +\%Y-\%m-\%d`-cron.log 2>&1
```
