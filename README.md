# fullstack.ai

This repository has been archived. Please look for better examples if you want to deploy ML-driven application.

## UI

<p align="center">
<image src="https://github.com/xadrianzetx/fullstack.ai/blob/master/gifs/faiui.gif"></image>
</p>


## API

<p align="center">
<image src="https://github.com/xadrianzetx/fullstack.ai/blob/master/gifs/faiapi2.gif"></image>
</p>

## Run

In order to deploy, you'll need to get mapbox API key [here.](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/) Then in project directory run

```
echo MAPBOX_API_KEY=your.api.key > .env && \
docker pull nginx:latest && \
docker-compose up --build -d
```

Nginx configuration maps reverse proxy server to port ```80```

## API guide

### GET valid station id

```curl -i "localhost:80/api/stations"```

### GET predicted trip time between two stations

<pre>
"localhost:80/api?start=<i>start_id</i>&end=<i>end_id</i>"
</pre>

### Parameters

* ```start_id``` (required) Valid start station id
* ```end_id``` (required) Valid end station id

### Example

```curl -i "localhost:80/api?start=73&end=39"```