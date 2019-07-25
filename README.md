###
Mozio

# Project Setup
You can setup the project as following
- Start the docker containers by running `docker-compose up`
- Run the django migrations inside the container
- Create Elasticsearch index by running `./manage.py search_index --rebuild`
inside the container.

# API Documentation
API Documentation can be found here:
https://safwan.docs.stoplight.io/service-area/service-area-list

# Deployment
Its deployed using Dokku in Digitalocean.
http://139.59.27.97.nip.io:49359/