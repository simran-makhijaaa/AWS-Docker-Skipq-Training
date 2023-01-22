
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
* Create and populate a URL table in DynamoDB.
* Create API lambda function
* Define CRUD (Create, Read, Update, Delete) operations in API Lambda Function.
* Define API gateway on API lamda function
* Add CRUD methods in API gateway
* Take urls from URL table in Web health lambda



## Installation

```bash
# Clone this repository
$ git clone https://github.com/simran2022skipq/Sirius_Python.git

# Go into the repository
$ cd Simran_Makhija/Sprint4

# Install requirements
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt

# Push code to github and run pipeline stack
$ cdk synth && cdk deploy SimranPipelineStack
```

## Demo

- <b> API Actions </b>

![image](https://user-images.githubusercontent.com/113733173/208581231-fd38fbe6-ab8c-41c3-b1c2-5eb07fa8908d.png)




- <b> Get method, when table is empty </b>

![get method no record](https://user-images.githubusercontent.com/113733173/208581309-1c098bc5-ba31-4989-b404-02de4437518f.png)




- <b> Get method </b>

![get ](https://user-images.githubusercontent.com/113733173/209066261-6d785eb7-2992-440f-b4d6-b85b6bf37add.png)




- <b> Post method </b>


![post url](https://user-images.githubusercontent.com/113733173/209066295-7d717d50-c1c7-42b9-be8b-f9b3082a5b18.png)




- <b> Delete method </b>

![delete](https://user-images.githubusercontent.com/113733173/209066760-0b9eb23a-277c-43bf-bea0-b84e666c602d.png)



- <b> Put / Update method </b>

![put](https://user-images.githubusercontent.com/113733173/209066880-f6ecb44d-5fe7-423a-a203-f911f3bcdb02.png)




- <b> API Table </b>

![image](https://user-images.githubusercontent.com/113733173/209066616-5e8c0eb1-6df6-45b0-a9ae-063334c057e2.png)

