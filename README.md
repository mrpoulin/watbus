# EasyGRT

EasyGRT is a web application to summarize and display bus stop times in a useful way.
It is written to use Grand River Transit's GTFS data.

## Getting Started

### Installing Python

Make sure you have python 2.7.4 installed and configured. This project is not using python 3+.

### Installing Django

This project is using Django 1.5. Please see [Installing Django 1.5](https://docs.djangoproject.com/en/dev/topics/install/#installing-official-release)

#### Django Setup

**Database**: SQLite

### Project Setup

To download the relevant GTFS data and import it to the database, run the setup bash script in the main directory.
The setup script runs two admin commands, getdata and importdata, which can be run individually to fetch the GTFS data and sync it to the DB respectively. 

#### Dependencies

**DSE**: https://bitbucket.org/weholt/dse4
