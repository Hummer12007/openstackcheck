import json
import socket

from io import StringIO

import paramiko

import openstackcheck.config as cfg
import openstackcheck.resources.nova as nv

from openstackcheck import OSCInvariantError
from openstackcheck.resources.ctx import test

def check_ssh(ctx):
    pkey = paramiko.RSAKey.from_private_key(StringIO(ctx.keypair.private_key))

    username = cfg.env.str('NOVA_SERVER_USERNAME', 'root')

    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ctx.floating_ip.floating_ip_address,
                    username=username, pkey=pkey,
                    timeout=5,
                    # workaround for dropbear
                    disabled_algorithms = {'pubkeys':['rsa-sha2-512','rsa-sha2-256']})
            _, out, __ = ssh.exec_command('curl http://169.254.169.254/openstack/latest/meta_data.json', timeout=10)
            meta = json.load(out)
            if meta['name'] != nv.DEFAULT_SERVER_NAME:
                raise ValueError('Invalid server name in metadata.json')
    except socket.error:
        return False

    return True

@test('Testing SSH connectivity with security groups')
def test_ssh_security(ctx):
    print('Checking ssh connectivity doesn\'t work')
    if check_ssh(ctx):
        raise OSCInvariantError('SSH was not supposed to work, but it worked')

    ctx.acquire('server_sg', nv.get_server_sg(ctx))

    print('Checking ssh connectivity works')
    if not check_ssh(ctx):
        raise OSCInvariantError('SSH was supposed to work, but it didn\'t')
