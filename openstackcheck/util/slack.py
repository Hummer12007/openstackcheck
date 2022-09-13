import json
import requests

from openstackcheck.config import env

slack_webhook_url = env.str('SLACK_WEBHOOK_URL')

def slack_report(error_stack):
    error_header = 'The following error(s) have occured during the smoke test:'

    error_message = {
        'text': error_header,
        'blocks': [
            {'type': 'section', 'text': {'type': 'mrkdwn', 'text': f'*{error_header}*\n'}},
        ],
    }

    for error in error_stack:
        description = f'{error.error_type.value} error for {"test" if error.error_type.value == "Test" else "resource"} *{error.resource}*:\n`{error.exception.__class__.__name__}`: {error.exception}\n```{error.traceback}```'
        error_message['blocks'].append({
            'type': 'section',
            'text': {'type': 'mrkdwn', 'text': description}
        })

    requests.post(slack_webhook_url, json.dumps(error_message), timeout=30)
