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

Consider that you are getting events in the format [{"event1":{"attr1": value }}] from different APIs.
* How will you parse the event to get the value?
* How will you return 10 latest events when required?


## Design


![AWS_Design_2](https://user-images.githubusercontent.com/113733173/206343272-c274f466-7a65-46de-b45f-2c66a78a54e5.png)


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

- <b> API POST Request passing attr1 = 40 </b>

![image](https://user-images.githubusercontent.com/113733173/206936965-f6514a43-5064-4815-a2ce-642b4a50f9a4.png)


- <b> API GET Request </b>

![image](https://user-images.githubusercontent.com/113733173/206937000-b2977721-5c88-4384-af04-55a86aed950f.png)


- <b> Dynamo DB table </b>

![image](https://user-images.githubusercontent.com/113733173/206937036-20454fd8-e59f-4236-8e8f-b78f7fdca2cb.png)



