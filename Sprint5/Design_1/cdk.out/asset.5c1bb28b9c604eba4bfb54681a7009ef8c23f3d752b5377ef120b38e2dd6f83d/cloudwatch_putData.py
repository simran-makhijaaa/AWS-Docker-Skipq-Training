import boto3
import os

class AWSCloudWatch:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
        self.sns_arn = os.environ["sns_arn"]
    
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data

    """
    Creating template for Metric data in CloudWatch
        Parameters:
            metric_name (str) - Name of the metric.
            namespace (str) - Namespace of the metric.
            dimensions ([Mapping[str, Any]]) - Dimensions of the metric.
            value (float) - Value what we get from url
    """
    def cloudwatch_metric_data(self , namespace , metric_name , dimensions, value):

        """CloudWatch Data Template"""
        
        response = self.client.put_metric_data(
            Namespace= namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'Value': value,
                },
            ]
        )

        self.client.put_metric_alarm(
            AlarmName = "SimranAPIDesignAlarm",
            ComparisonOperator = "GreaterThanThreshold",
            EvaluationPeriods = 1,
            MetricName = metric_name,
            Namespace = namespace,
            Period = 60,
            Statistic = "Average",
            Threshold = 10,
            Dimensions = dimensions,
            ActionsEnabled = True,
            AlarmActions = [self.sns_arn]
        )