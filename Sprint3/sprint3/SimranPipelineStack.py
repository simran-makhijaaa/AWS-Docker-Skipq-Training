from aws_cdk import (
    pipelines as pipelines_,
    Stack,
    aws_codepipeline_actions as actions_,
    SecretValue as SecretValue_
)
from constructs import Construct
from sprint3.SimranStage import SimranStage


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
                                    commands=["cd Simran_Makhija/Sprint3/",
                                    "npm install -g aws-cdk",
                                    "pip install -r requirements.txt",
                                    "pip install -r requirements-dev.txt",
                                    "cdk synth"],
                                    primary_output_directory = "Simran_Makhija/Sprint3/cdk.out"
                                )
        
        # Creating a pipeline
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        pipeline = pipelines_.CodePipeline(self, "SimranPipelineStack3", synth=synth)

        # Creating stages
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        betaTesting = SimranStage(self, "Beta")
        prod = SimranStage(self, "Prod")
        
        # Adding beta stage to pipeline with unit tests
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/AddStageOpts.html
        pipeline.add_stage(betaTesting, pre=[
                            pipelines_.ShellStep("Synth",
                                    input=source,
                                    commands=["cd Simran_Makhija/Sprint3/",
                                    "npm install -g aws-cdk",
                                    "pip install -r requirements.txt",
                                    "pip install -r requirements-dev.txt",
                                    "python3 -m pytest",
                                    "cd tests/integration",
                                    "python3 integration.py"])           
                        ])

        # Adding prod stage to pipeline with manual approval
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/AddStageOpts.html
        pipeline.add_stage(prod, pre=[pipelines_.ManualApprovalStep("ApproveToProd")])
