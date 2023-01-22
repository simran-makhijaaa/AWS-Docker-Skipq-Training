# Welcome to AWS Design Day 1 Python project!


[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-3810/)
[![AWS cdk 2.51.1](https://img.shields.io/badge/aws_cdk_lib-2.51.1-yellow.svg)](https://pypi.org/project/aws-cdk-lib/2.51.1/)
[![Constructs 10.1.165](https://img.shields.io/badge/constructs-10.1.165-red.svg)](https://pypi.org/project/constructs/10.1.165/)



## Table of Contents

- [Task](#task)
- [Design](#design)
- [Installation](#installation)
- [Demo](#demo)


## Task

Consider that you are getting an event response as {“arg1”: 10} from an API.
* a) Make an AWS app that generates an alarm if arg1 > 10.
* When the alarm is raised, send an email to a dummy account.


## Design


![AWS_Design_1](https://user-images.githubusercontent.com/113733173/206018568-5fa8b545-2bb5-4606-90c3-5b5a6bc5b351.png)


## Installation

```bash
# Clone this repository
$ git clone https://github.com/simran2022skipq/Sirius_Python.git

# Go into the repository
$ cd Simran_Makhija/Sprint5/Design_1

# Install requirements
$ pip install -r requirements.txt

# Convert code to CloudFormation
$ cdk synth

# Deploy code to AWS
$ cdk deploy
```

## Demo

- <b> API Gateway </b>

![image](https://user-images.githubusercontent.com/113733173/206019307-1496101c-e20d-41d4-b558-a39ba8ffbe9b.png)


- <b> Test API with argument "13" </b>

![image](https://user-images.githubusercontent.com/113733173/206019626-4881b0d0-1912-471d-93c7-486c6d6c1575.png)


- <b> Alarm </b>
