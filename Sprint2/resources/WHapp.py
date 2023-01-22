import urllib3
import datetime
from cloudwatch_putData import AWSCloudWatch
import constants as constants


"""
Creating function to get availability and latency of urls, and put it in CloudWatch

    Return:
        Dictionary of availability and latency values
"""
def lambda_handler(event, context):

    """CloudWatch object"""
    cloudwatch_object = AWSCloudWatch()

    values = {}
    availability = []   
    latency = []
    for url in constants.urls:
        av = getAvail(url)
        availability.append(av)
        la = getLatency(url)
        latency.append(la)

        """ Sending data to CloudWatch"""
        dimensions = [{'Name': 'URL','Value': url}]
        cloudwatch_object.cloudwatch_metric_data(constants.namespace , constants.AvailibiltyMetric , dimensions, av)
        cloudwatch_object.cloudwatch_metric_data(constants.namespace , constants.LatencyMetric , dimensions, la)

    values["availability"] = availability
    values["latency"] = latency

    
    return values

"""
Getting availability of a url
    Parameters:
        url (str) - Url of a website

    Return:
        number (float) - 1.0 or 0.0
"""
def getAvail(u):
    http = urllib3.PoolManager()
    response = http.request('GET', u)
    response.status
    if response.status == 200:
        return 1.0
    else:
        return 0.0

"""
Getting latency of a url
    Parameters:
        url (str) - Url of a website

    Return:
        latency seconds (float) - time a website takes to load
"""
def getLatency(u):
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request('GET', u)
    end = datetime.datetime.now()
    delta = end - start
    latency_sec = round(delta.microseconds * .000001 , 6)
    return latency_sec
    

