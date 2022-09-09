import os
import json
import socket
import traceback

from io import StringIO

import paramiko

import openstack.connection as osc

import openstack.identity.v3 as oi
import openstack.block_storage.v3 as ob
import openstack.compute.v2 as oc
import openstack.network.v2 as on

import openstackcheck.nova as nv
import openstackcheck.glance as gl
import openstackcheck.keystone as ks
import openstackcheck.cinder as cd
import openstackcheck.neutron as nt
import openstackcheck.config as cfg

from openstackcheck.auth import get_admin_auth
from openstackcheck.base import BaseContext

class OSCContext(BaseContext):
    admin: osc.Connection

    domain: oi.endpoint.Endpoint
    project: oi.project.Project
    username: str
    password: str
    user: oi.user.User

    auth: osc.Connection

    router: on.router.Router
    network: on.network.Network
    subnet: on.subnet.Subnet
    interface: None

    image_id: str
    volume: ob.volume.Volume

    flavor: int
    keypair: oc.keypair.Keypair
    private_key_path: str
    server: oc.server.Server

    floating_ip: on.floating_ip.FloatingIP
    server_floating_ip: None

    sg: on.security_group.SecurityGroup
    server_sg: None


def do_tests(ctx):
    ctx.acquire_res('admin', get_admin_auth())

    domain = ctx.acquire('domain', ks.get_domain(ctx))
    project = ctx.acquire('project', ks.get_project(ctx))
    user = ctx.acquire('user', ks.get_user(ctx))
    auth = ctx.acquire_res('auth', ks.get_auth(ctx))

    router = ctx.acquire('router', nt.get_router(ctx))
    network = ctx.acquire('network', nt.get_network(ctx))
    subnet = ctx.acquire('subnet', nt.get_subnet(ctx))
    interface = ctx.acquire('interface', nt.get_interface(ctx))

    image_id = ctx.acquire_res('image_id', gl.get_image_id(ctx))
    volume = ctx.acquire('volume', cd.get_volume(ctx))

    keypair = ctx.acquire('keypair', nv.get_keypair(ctx))
    flavor = ctx.acquire_res('flavor', nv.get_flavor(ctx))
    server = ctx.acquire('server', nv.get_server(ctx))

    floating_ip = ctx.acquire('floating_ip', nt.get_floating_ip(ctx))
    server_floating_ip = ctx.acquire('server_floating_ip', nv.get_server_floating_ip(ctx))

    sg = ctx.acquire('sg', nt.get_sg(ctx))

    print('Checking ssh connectivity doesn\'t work')
    if check_ssh(ctx):
        raise Exception('SSH was not supposed to work, but it worked')

    server_sg = ctx.acquire('server_sg', nv.get_server_sg(ctx))

    print('Checking ssh connectivity works')
    if not check_ssh(ctx):
        raise Exception('SSH was supposed to work, but it didn\'t')

    print('SUCCESS! Everything is working')

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


def main():
    with BaseContext() as ctx:
        try:
            do_tests(ctx)
        except:
            print('An error occured, cleaning up')
            print(traceback.format_exc())

if __name__ == '__main__':
    main()
