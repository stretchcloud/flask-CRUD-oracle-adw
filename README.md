# Flask CRUD API using Oracle Data Warehouse


## Built With

* [Python 3](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Docker](https://www.docker.com/)
* [Oracle Autonomous Data Warehouse](https://cloud.oracle.com/en_US/datawarehouse)

## Prerequisites

You will need the following things properly installed on your computer:

* [Git](http://git-scm.com/)
* [Docker](https://www.docker.com/)
* [Oracle Autonomous Data Warehouse Instance](https://cloud.oracle.com/en_US/datawarehouse)

## Setup

This instruction is to show, how to run the developed API in either inside a Docker Container or inside a Kubernetes Cluster.
  
This is split in two buckets. Firstly we will see how to deploy it in Docker Container and the second part will focus on Kubernetes.

### 1. Fork this repository, download the wallet, update the credentials & Deploy the build the Docker Container

First of all, let's clone this repository

`https://github.com/stretchcloud/flask-CRUD-oracle-adw`

`cd flask-CRUD-oracle-adw`

Getting the Autonomous Data Warehouse Wallet files

* Navigate to your ADW instance on the Oracle Cloud Infrastructure Console
* Click 'DB Connection'
* Download the Client Credentials (Wallet)
* Unzip the files and place them in the `wallet` folder in this project

Updating Python API

* Update `createtable.py` with the ADW credentials. You will get the DB Connection name from the tnsnames.ora from your wallet folder.
* Update the `importcsv.py` with the ADW credentials, similar to createtable.

Build, Tag and Push the Docker Container to the Docker Hub

`docker build -t flaskapioracleadw:latest .`

`docker tag flaskapioracleadw:latest jit2600/flaskapioracleadw:latest`

`docker push jit2600/flaskapioracleadw:latest`

Your Docker Image is ready. You can either run it in daemon mode or interactive run.

`docker run --name flaskapioracleadw -p 5000:5000 flaskapioracleadw:latest` => Run this if you want to debug the output.

`docker run --name flaskapioracleadw -d -p 5000:5000 flaskapioracleadw:latest` => Non interactive, daemon mode.

Use `curl` to test the endpoint

`curl -X GET -H "Content-type: application/json" http://127.0.0.1:5000/people`

`curl -X GET -H "Content-type: application/json" http://127.0.0.1:5000/people/{uuid}`

`curl -X DELETE -H "Content-type: application/json" http://127.0.0.1:5000/people/{uuid}`

`curl -X POST -H "Content-type: application/json" -d '{"survived" : "1", "passengerClass" : "3", "name" : "Sandhya Sarkar", "sex" : "Female", "age" : "104", "siblingsOrSpousesAboard" : "0", "parentsOrChildrenAboard" : "0", "fare" : "40"}' http://127.0.0.1:5000/people/`

`curl -X PUT -H "Content-type: application/json" -d '{"survived" : "1", "passengerClass" : "3", "name" : "Sandhya Sarkar", "sex" : "Female", "age" : "104", "siblingsOrSpousesAboard" : "0", "parentsOrChildrenAboard" : "0", "fare" : "100"}' http://127.0.0.1:5000/people/{uuid}`



### 2. Deploy it to Kubernetes

We have already built the Docker Image and pushed it to Docker Registry. Also, we have supplied the flaskapp Deployment and Service YML. Create a deployment and a service and you will be good to go.

`kubectl create -f flaskapp-deployment.yml`

`kubectl create -f flaskapp-service.yml`

`kubectl get deployments` => Check whether the app has been deployed

`kubectl get service` => Check whether the service has been deployed

`kubectl get pods` => Check whether the POD is up and running 

`kubectl port-forward service/apiapp 5000 5000` => Create the port-forward to access the API. This is required if you are using NodePort.

At this point, you can use the same curl option to test the API endpoint.

### Swagger
We have included the Swagger definition of the entire API as well. Once you deploy it to either Docker or Kubernetes, just browse the <IP:5000/swagger> and you can see the entire definition.
