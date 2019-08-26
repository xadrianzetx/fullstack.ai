[![Build Status](https://travis-ci.org/xadrianzetx/fullstack.ai.svg?branch=master)](https://travis-ci.org/xadrianzetx/fullstack.ai)

# fullstack.ai

End-to-end machine learning project showing key aspects of developing and deploying real life machine learning driven application.

## Hosting

Running example is currently hosted [here.](https://fullstackai.pythonanywhere.com/)

## POC

* EDA, data manipulation an preparation
* Scraping additional features from external sources
* Iterative process of building ML model
* Wrapping it as Python module as transition from dev colab notebooks to prod code
* Using this module in Flask based microservice
* Contenerizing it with Docker and deploying using Nginx reverse proxy server orchestrated with Docker Compose

This basically covers most of ML tech stack up to CI/CD pipeline.

I'll be using [SF Bay Area Bike Share](https://www.kaggle.com/benhamner/sf-bay-area-bike-share) dataset to model duration of bike travel across San Francisco. This dataset is bit dated and task itself is probably bit banal, but hey, this project is all about tech stack and leveraging different tools and ml techniques to achive my goal - a web based ml driven bike trip advisor with trip time prediction.

## Notebooks

* [Introduction and database](https://colab.research.google.com/drive/1CTkqQqJ0AeOVOyOt72wXPRA4EAelczT7)
* [EDA and feature engineering](https://colab.research.google.com/drive/1XqpKyyOcJvene56QvdpDkheXIPAPR4Zq)
* [Final preprocessing and models](https://colab.research.google.com/drive/1ScEaYTg3dOSH0qnIAvBZ7e-qSVSoxJG1)
* [Bayesian optimization](https://colab.research.google.com/drive/1ZcOH0TnmNkCMbDoyjtXZCTyWQjEL_jEx)
* [Model Evaluation](https://colab.research.google.com/drive/1piEA-OwvmfkGna-rNfiE2-WHUVUxrwUS)


## UI

<p align="center">
<image src="https://github.com/xadrianzetx/fullstack.ai/blob/master/gifs/faiui.gif"></image>
</p>


## API

<p align="center">
<image src="https://github.com/xadrianzetx/fullstack.ai/blob/master/gifs/faiapi2.gif"></image>
</p>

## Run

In order to deploy, you'll need to get mapbox API key [here.](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/) Then run

```
cd static/js && touch config.js
```

```config.js``` should look like this

```
const config = {
    'mapboxApiKey': your.api.key.here
}
```

Having done this, app is now ready to deploy, so go to top of directory and build Nginx and app containers using

```
docker pull nginx:latest && docker-compose up --build -d
```

Nginx configuration maps reverse proxy server to port ```80```

## API guide

API for hosted example is available at 

``` https://fullstackai.pythonanywhere.com/api```

### GET valid station id

```curl -i "https://fullstackai.pythonanywhere.com/api/stations"```

### GET predicted trip time between two stations

<pre>
"https://fullstackai.pythonanywhere.com/api?start=<i>start_id</i>&end=<i>end_id</i>
</pre>

### Parameters

* ```start_id``` (required) Valid start station id
* ```end_id``` (required) Valid end station id

### Example

```curl -i "https://fullstackai.pythonanywhere.com/api?start=73&end=39"```