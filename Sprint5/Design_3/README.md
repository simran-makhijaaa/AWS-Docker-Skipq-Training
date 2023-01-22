# Welcome to AWS Design Day 3 !


## Table of Contents

- [Task 1](#task-1)
- [Task 2](#task-2)


## Task 1

1) How would you automate deployment (e-g on AWS) for a system that has source code in a repo?
2) How do we generate an artifact from the repo that gets published and later is used in some services?
3) Are there more than one solutions?


#### Question 1:

<b> How would you automate deployment (e-g on AWS) for a system that has source code in a repo.? </b>

The deployment can be automated by using CI/CD pipeline. The pipeline has following stages:
- <b> Source stage: </b> When code is commited, the CI/CD pipeline is triggered.
- <b> Build/Test Stage: </b> Code is built and synthesized in this stage. After that tests are performed such as unit test, integration test and functional test.
- <b> Deploy Stage: </b> If the tests are passed successfully then deploy stage is triggered.


#### Question 2:

<b> How do we generate an artifact from the repo that gets published and later is used in some services.? </b>

- An artifact is generated from the repo by using CodeBuild within the pipeline. 
- The artifacts are stored in s3 bucket.
- The urls of artifacts can be shared and used in some services.


#### Question 3: 

<b> Are there more than one solutions.? </b>

yes, there are more than 1 solutions, by using other AWS services or 3rd party services such as Jenkins.




## Task 2

Deploy, maintain and rollback pipeline for an artifact deployment e-g lambda package, docker image etc.
1) If the latest deployment is failing, why do you think that is?
2) How will you rollback? 
3) How do you reduce such failures so there is less need to rollback?


#### Question 1:

<b> If the latest deployment is failing, why do you think that is.? </b>

There might be many reasons for the failure of latest deployment, few of them are:
- Not defining the policies and permissions.
- Pipeline does not have access to the repository.
- Deployment might fail because of different regions.


#### Question 2:

<b> How will you rollback.? </b>

We can rollback by generating alarms, if an alarm is raised on specified threshold, then it will rollback with the help of deployment groups.


#### Question 3:

<b> How do you reduce such failures so there is less need to rollback.? </b>

We can reduce such failures by having multiple stages with different tasks/tests across multiple regions.
