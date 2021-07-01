# monitoring

# fetch the image

https://hub.docker.com/r/alexmercer/graphite-grafana

```
docker pull alexmercer/graphite-grafana
```

# run the image mounting volumens for persistent data storage in /var/lib/gmonitor

```
docker run -v /var/lib/gmonitor/graphite/whisper:/var/lib/graphite/storage/whisper \
           -v /var/lib/gmonitor/graphite/conf:/var/lib/graphite/conf \
           -v /var/lib/gmonitor/grafana/data:/usr/share/grafana/data \
           -p 2003:2003 \
           -p 2004:2004 \
           -p 3000:3000 \
           -p 8080:80 \
           -d alexmercer/graphite-grafana

```

# navigate to webserver admin:admin

http://localhost:3000/login/
