# uw-mailman3-web
UW themed mailman3-web, with accessibility fixes.

## System Requirements

- Python (3+)
- Docker

## Development Stack

- Django (3.2)
- Bootstrap (5.1.3)
- Bootstrap Icons (1.7.0)

## Setup

Create a directory for running your project

    $ mkdir mailman3

Clone core and web repos in the directory

    $ cd mailman3
    $ git clone git@github.com:uw-it-aca/uw-mailman3-core.git
    $ git clone git@github.com:uw-it-aca/uw-mailman3-web.git

## Development (using Docker)

Go to the web repository

    $ cd uw-mailman3-web

Copy the sample env configuration and override any vars you might want.

    $ cp .env.sample .env

Run the Docker container

    $ docker-compose up --build

View your application using your specified port number in the .env file

    Demo: http://localhost:8000/
