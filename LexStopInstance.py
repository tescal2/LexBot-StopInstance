import boto3
import logging
import os
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

" -----Main handler ----- "

def handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)


def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'StopInstance':
        return stop_ec2(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')

def close(session_attributes,fulfillment_state,message):
    response = {
        'sessionAttributes':session_attributes,
        'dialogAction':{
            'type': 'Close',
            'fulfillmentState':fulfillment_state,
            'message':message
        }
    }

    return response

def stop_ec2(intent_request):
    card_title = "Stopping"
    output_session_attributes = {}
    slots = intent_request['currentIntent']['slots']
    instance_value = intent_request['currentIntent']['slots']['Instance']
    instanceValue = instance_value.lower()
    ec2 = boto3.client('ec2', region_name='us-east-1')
    response = ec2.describe_instances()
    insId = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            for i in instance["Tags"]:
                if (i["Value"] == instanceValue):
                    insId.append(instance["InstanceId"])
    ec2.stop_instances(InstanceIds=insId)
    return close(output_session_attributes, 'Fulfilled',
            {'contentType':'PlainText','content':'Success! Stopping Your Server Now.'})

