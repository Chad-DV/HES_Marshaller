# JAVA_HES_POWERSHARE_MARSHALLER

Takes data from the Java Meter aquisitioning script (published to SGate) and passes it to a DB and Thingsboard for Visualisation

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Future-Features](#future-features)

## Introduction

This service Subscribes to a MQTT broker Topic, listens to any data, and publishes to a different MQTT Broker while simultaniously inserting the data into a MySQL database. This is specifically catered for the data being published from the Java meter aquisitiong script see (REMOVED)

## Installation

Copy jes_ps_marshaller.tar to your linux server (SCP or SFTP) <br/>
Navigate to the direcory and extract (sudo docker load -i jhes_ps_marshaller.tar) <br/>
Tag the file (sudo docker tag {IMAGE_ID} {NAME_FOR_FILE}:{YOUR_TAG}) <br>

## Usage

Run the container Image. (Make sure the path exists) <br/>
docker run -d -v {PATH_TO_LOGS}:/logs {IMAGE_ID} <br/>
docker logs {CONTAINER_ID} to view any logs 

## Configuration
To Point the script to Different brokers or DB's change the settings in the config.json file found in the root file directory.

## Future-Features
ports for brokers are not catered for is the ports in config.json change it may cause the main scriot to fial.


### Authored by
chad.devilliers@igrid.co.za
28/02/2024