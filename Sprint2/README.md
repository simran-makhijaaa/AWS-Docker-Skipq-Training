
# Welcome to Web Health Python project!



[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-3810/)
[![AWS cdk 2.51.1](https://img.shields.io/badge/aws_cdk_lib-2.51.1-yellow.svg)](https://pypi.org/project/aws-cdk-lib/2.51.1/)
[![Constructs 10.1.165](https://img.shields.io/badge/constructs-10.1.165-red.svg)](https://pypi.org/project/constructs/10.1.165/)



## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Demo](#demo)


## Introduction

In this sprint, I have done following tasks:
* Create a lambda function
* Find the availaibility and latency of 4 urls
* Cron job the lambda function for every 60 minutes
* Add availabilities and latencies to metrics and publish it to the CloudWatch
* Add alarms to CloudWatch metrics
* Send notifications to email if alarm is triggered
* Create dynamo db table
* Send alert notification to db


## Installation

```bash
# Clone this repository
$ git clone https://github.com/simran2022skipq/Sirius_Python.git

# Go into the repository
$ cd Simran_Makhija/Sprint2

# Install requirements
$ pip install -r requirements.txt

# Convert code to CloudFormation
$ cdk synth

# Deploy code to AWS
$ cdk deploy
```

## Demo

- <b>Metrics</b>

![image](https://user-images.githubusercontent.com/113733173/202990482-6d34d06c-07b1-45e2-9819-9b50adf5d99c.png)


- <b>Alarms</b>

![image](https://user-images.githubusercontent.com/113733173/202990394-02bf2090-905f-4a43-8e2c-ca03b2c3884a.png)


- <b>Dynamo DB Table </b>

![image](https://user-images.githubusercontent.com/113733173/203159706-50b4cf90-ee49-4554-a0e6-88124aabd957.png)

