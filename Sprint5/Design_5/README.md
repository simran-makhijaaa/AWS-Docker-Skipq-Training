# Welcome to AWS Design Day 5 Python project!


[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-3810/)
[![AWS cdk 2.51.1](https://img.shields.io/badge/aws_cdk_lib-2.51.1-yellow.svg)](https://pypi.org/project/aws-cdk-lib/2.51.1/)
[![Constructs 10.1.165](https://img.shields.io/badge/constructs-10.1.165-red.svg)](https://pypi.org/project/constructs/10.1.165/)



## Table of Contents

- [Task](#task)
- [Design](#design)
- [Installation](#installation)
- [Demo](#demo)


## Task

<b> Design & Develop </b> - Suppose there are 10 files uploading to S3 bucket each day. For each file received on cloud storage, you have a mechanism to process the file. During the processing, your code parses the text and counts the number of times each word is repeated in the file. For example, in the following text: “Hello World and Hello There”, your code should be able to say that "hello" has been used twice, "world" has occurred once and so on. Then it will store the results in some storage and email to some email address after successful processing.


## Design


![AWS_Design_5](https://user-images.githubusercontent.com/113733173/207739298-c9944407-4771-4ecf-91b6-d19485b96355.png)



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

- <b> Lambda cloud watch </b>


File content is "Hello Simran Hello Lambda Hello Simran"
Output is: word and its occurence



![image](https://user-images.githubusercontent.com/113733173/207739698-478e4cf9-f22b-4fc5-855f-b4913a71b720.png)




- <b> S3 bucket for file uploading </b>



![image](https://user-images.githubusercontent.com/113733173/207739455-9e8e0d92-e480-486c-856b-dd7d2e1aa543.png)




- <b> S3 bucket for output file after we process the data </b>



![image](https://user-images.githubusercontent.com/113733173/207739858-6f772d8b-faf4-4920-86e7-4ddead995cc0.png)




- <b> Email notification after output file is uploaded to bucket </b>



![image](https://user-images.githubusercontent.com/113733173/207740034-a09b9770-446e-4f79-ac21-10a03a9d8760.png)


