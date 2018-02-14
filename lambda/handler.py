import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def define_challenge(event, context):
    logger.info(json.dumps(event))

    event['response']['issueTokens'] = True
    event['response']['failAuthentication'] = False

    return event
