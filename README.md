## Openstackcheck

This utility can perform a set of checks for basic OpenStack functionality.

It currently tests Keystone, Glance, Cinder, Neutron and Nova.

## Installation

`python setup.py install` OR `pip install .`

## Usage

`openstackcheck`, having necessary environment variables set in the environment or an .env file

## Dependencies

- openstacksdk
- paramiko
- environs
- requests


## Configuration

openstackcheck can be configured using the following environment variables (can be stored in an `.env` file in the working directory):

- `KEYSTONE_URL` (required) - URL of the Keystone service
- `KEYSTONE_ADMIN_TOKEN` (required, unless username + password provided) - admin token for authorization
- `KEYSTONE_ADMIN_USERNAME` (required, unless token provided) - admin username for authorization
- `KEYSTONE_ADMIN_PASSWORD` (required, unless token provided) - admin password for authorization
- `KEYSTONE_ADMIN_PROJECT` (required) - ID of the admin project
- `KEYSTONE_USER_DOMAIN` - domain of the admin user
- `KEYSTONE_PROJECT_DOMAIN` - domain of the admin project
- `SMOKETEST_DOMAIN` - domain name to use for the tests, defaults to `smokecheck`
- `SMOKETEST_PROJECT` - project name to use for the tests, defaults to `smokecheck`
- `SLACK_WEBHOOK_URL` (required) - webhook URL for Slack notifications
- `GLANCE_IMAGE` - Glance image name or ID to use for server creation (defaults to first found image)
- `NOVA_FLAVOR` - flavor to use for vm, alternatively, the lowest sized one enough to launch the image is selected.
- `NEUTRON_EXTERNAL_NET` - publically accessible network name (defaults to `public`)

Example can be found in `.env.example`.
