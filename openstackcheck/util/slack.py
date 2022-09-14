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
        description = f'{error.context.type.value} error for {"test" if error.context.type.value == "Test" else "resource"} *{error.context.resource}{f" ({error.context.description})" if error.context.description else ""}*:\n`{error.exception.__class__.__name__}`: {error.exception}\n```{error.traceback}```'
        error_message['blocks'].append({
            'type': 'section',
            'text': {'type': 'mrkdwn', 'text': description}
        })

    requests.post(slack_webhook_url, json.dumps(error_message), timeout=30)
