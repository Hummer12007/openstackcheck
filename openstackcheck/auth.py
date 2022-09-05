from openstack import connection

from openstackcheck.config import env, keystone_url

# Keystone admin credentials
keystone_token = env.str('KEYSTONE_ADMIN_TOKEN', None)

if not keystone_token:
    keystone_username = env.str('KEYSTONE_ADMIN_USERNAME')
    keystone_password = env.str('KEYSTONE_ADMIN_PASSWORD')

keystone_project = env.str('KEYSTONE_ADMIN_PROJECT')
keystone_user_domain = env.str('KEYSTONE_USER_DOMAIN', None)
keystone_project_domain = env.str('KEYSTONE_PROJECT_DOMAIN', None)

def get_admin_auth():
    auth = dict(auth_url=keystone_url, project_id=keystone_project)
    if keystone_user_domain:
        auth['user_domain_id'] = keystone_user_domain
    if keystone_project_domain:
        auth['project_domain_id'] = keystone_project_domain
    if keystone_token:
        auth['token'] = keystone_token
    else:
        auth['username'] = keystone_username
        auth['password'] = keystone_password

    return connection.Connection(auth=auth, identity_interface='public')
