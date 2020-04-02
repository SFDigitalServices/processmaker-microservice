# SFDS Process Maker microservice.py [![CircleCI](https://badgen.net/circleci/github/SFDigitalServices/processmaker-microservice/master)](https://circleci.com/gh/SFDigitalServices/processmaker-microservice) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/processmaker-microservice/badge.svg?branch=master)](https://coveralls.io/github/SFDigitalServices/processmaker-microservice?branch=master)

### Sample Usage
Install Pipenv (if needed)
> $ pip install --user pipenv

Install included packages
> $ pipenv install

Setup environment variables
> $ cp .env.example .env

Start WSGI Server
> (processmaker-microservice)$ pipenv run gunicorn 'service.microservice:start_service()'

Try with cURL 
> (processmaker-microservice)$ curl curl --location --request POST 'http://127.0.0.1:8000/cases/leaveRequest?workspace={workspace}' --header 'Content-Type: application/json' --data-raw '{"message": "hello world"}'
