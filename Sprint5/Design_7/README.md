# Welcome to AWS Design Day 7 Python project!


[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-3810/)
[![AWS cdk 2.51.1](https://img.shields.io/badge/aws_cdk_lib-2.51.1-yellow.svg)](https://pypi.org/project/aws-cdk-lib/2.51.1/)
[![Constructs 10.1.165](https://img.shields.io/badge/constructs-10.1.165-red.svg)](https://pypi.org/project/constructs/10.1.165/)



## Table of Contents

- [Task](#task)
- [Design](#design)
- [Installation](#installation)
- [Demo](#demo)


## Task

<b> Design & Develop </b> - What if we have a 15MB file that we have to upload on S3 using API gateway. We have the limitation that our API gateway has the maximum payload capacity of 10MB. How will you solve this problem?


## Design


![AWS_Design_7](https://user-images.githubusercontent.com/113733173/207783802-8e4d2c31-77ed-438b-8b40-7ec35498d74a.png)



## Installation

```bash
# Clone this repository
$ git clone https://github.com/simran2022skipq/Sirius_Python.git

# Go into the repository
$ cd Simran_Makhija/Sprint5/Design_5

# Install requirements
$ pip install -r requirements.txt

# Convert code to CloudFormation
$ cdk synth

# Deploy code to AWS
$ cdk deploy
```

## Demo

- <b> Rest API to get pre-signed url for uploading the file </b>

![image](https://user-images.githubusercontent.com/113733173/209072907-e8bed920-789d-438b-a71e-3978f7e86271.png)

