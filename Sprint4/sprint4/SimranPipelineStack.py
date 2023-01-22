from aws_cdk import (
    pipelines as pipelines_,
    Stack,
    aws_codepipeline_actions as actions_,
    SecretValue as SecretValue_,
    aws_codebuild as codebuild_
)
from constructs import Construct
from sprint4.SimranStage import SimranStage


class SimranPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Authenticating our github repo
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codepipeline_actions.html

        source = pipelines_.CodePipelineSource.git_hub("simran2022skipq/Sirius_Python", "main",
                                                        authentication = SecretValue_.secrets_manager("SimranToken", json_field="SimranToken"),
                                                        trigger = actions_.GitHubTrigger('POLL'))

        # Adding shell step to synthesize application
        #https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.pipelines.ShellStep.html
        synth = pipelines_.ShellStep("Synth",
                                    input=source,
                                    commands=["cd Simran_Makhija/Sprint4/",
                                    "npm install -g aws-cdk",
                                    "pip install -r requirements.txt",
                                    "pip install -r requirements-dev.txt",
                                    "cdk synth"],
                                    primary_output_directory = "Simran_Makhija/Sprint4/cdk.out"
                                )
        
        # Creating a pipeline
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        pipeline = pipelines_.CodePipeline(self, "SimranPipelineStack4", synth=synth)

        # Defining the shell step for unit, integration and functional test in beta stage 
        beta_stage_pre_tests = pipelines_.ShellStep("Synth",
                                    input=source,
                                    commands=["cd Simran_Makhija/Sprint4/",
                                    "npm install -g aws-cdk",
                                    "pip install -r requirements.txt",
                                    "pip install -r requirements-dev.txt",
                                    "python3 -m pytest"
#                                     "cd tests/integration",
#                                     "python3 integration.py"
                                             ])

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/README.html 
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodeBuildStep.html 
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codebuild/README.html 
        # https://docs.aws.amazon.com/codebuild/latest/userguide/sample-docker-custom-image.html 
        pyresttest_api = pipelines_.CodeBuildStep("SimranPyresttest",
                                   commands=[],
                                   build_environment = codebuild_.BuildEnvironment(
                                                        build_image= codebuild_.LinuxBuildImage.from_asset(self, "Image", directory= "docker-images/").from_docker_registry(name="docker:dind"), 
                                                        privileged= True),
                                    partial_build_spec = codebuild_.BuildSpec.from_object({
                                                        "version": 0.2,
                                                        "phases": {
                                                        "install": {
                                                          "commands": [
                                                            "nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &",
                                                            "timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\""
                                                          ]
                                                        },
                                                        "pre_build": {
                                                          "commands": [
                                                            "cd Simran_Makhija/Sprint4/docker-images",
                                                            "docker build -t simranapitest ."
                                                          ]
                                                        },
                                                        "build": {
                                                          "commands": [
                                                            "docker images",
                                                            "docker run simranapitest"
                                                          ]
                                                        }
                                                      }
                                    }))

        # Creating stages
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        betaTesting = SimranStage(self, "Beta")
        prod = SimranStage(self, "Prod")
        
        # Adding beta stage to pipeline with unit tests
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/AddStageOpts.html
        pipeline.add_stage(betaTesting, pre=[beta_stage_pre_tests], post= [pyresttest_api])

        # Adding prod stage to pipeline with manual approval
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/AddStageOpts.html
        pipeline.add_stage(prod, pre=[pipelines_.ManualApprovalStep("ApproveToProd")])
