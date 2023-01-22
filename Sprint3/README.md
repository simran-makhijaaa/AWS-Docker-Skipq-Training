
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
* Create pipelines
* Add beta and prod stages to the pipeline
* Deploy the pipeline
* Write 5 unit tests
* Write 1 integration test
* Write 1 functional test
* Add unit test step in the beta stage
* Add manual approval step before the prod stage
* Create two metrics (duration and errors) for lambda web health
* Create alarms on those metrics
* Configure auto rollback if any of the metrics are in alarm




## Installation

```bash
# Clone this repository
$ git clone https://github.com/simran2022skipq/Sirius_Python.git

# Go into the repository
$ cd Simran_Makhija/Sprint3

# Install requirements
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt

# Push code to github and run pipeline stack
$ cdk synth && cdk deploy SimranPipelineStack
```

## Demo

### Pipeline

- <b> Source & Build </b>

![image](https://user-images.githubusercontent.com/113733173/204151567-f4110097-fb4a-479a-9912-ac6f7b4aa745.png)


- <b> UpdatePipeline & Assets </b>

![image](https://user-images.githubusercontent.com/113733173/204151713-7e323104-ffdc-4bae-9442-a6310c9f8a08.png)


- <b> Beta Stage </b>

![image](https://user-images.githubusercontent.com/113733173/204151762-a0c6f268-982a-4f3f-8841-31841470d5e3.png)


- <b> Prod Stage </b>

![image](https://user-images.githubusercontent.com/113733173/204151800-08e70ac4-c01a-4ed5-affe-b442aeddaca2.png)
