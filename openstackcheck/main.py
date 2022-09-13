import openstack.connection as osc

import openstack.image.v2 as og
import openstack.compute.v2 as oc
import openstack.network.v2 as on
import openstack.identity.v3 as oi
import openstack.block_storage.v3 as ob

import openstackcheck.resources.nova as nv
import openstackcheck.resources.glance as gl
import openstackcheck.resources.cinder as cd
import openstackcheck.resources.neutron as nt
import openstackcheck.resources.keystone as ks

from openstackcheck import tests, OSCInvariantError

from openstackcheck.resources.auth import get_admin_auth
from openstackcheck.util.slack import slack_report
from openstackcheck.util.base_ctx import BaseContext
from openstackcheck.util.error_ctx import log_error, ErrorType, error_stack

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

    image: og.image.Image
    volume: ob.volume.Volume

    flavor: int
    keypair: oc.keypair.Keypair
    private_key_path: str
    server: oc.server.Server

    floating_ip: on.floating_ip.FloatingIP
    server_floating_ip: None

    sg: on.security_group.SecurityGroup
    server_sg: None


def initial_setup(ctx):
    ctx.acquire_res('admin', get_admin_auth())

    domain = ctx.acquire('domain', ks.get_domain(ctx))
    project = ctx.acquire('project', ks.get_project(ctx))
    user = ctx.acquire('user', ks.get_user(ctx))
    auth = ctx.acquire_res('auth', ks.get_auth(ctx))

    router = ctx.acquire('router', nt.get_router(ctx))
    network = ctx.acquire('network', nt.get_network(ctx))
    subnet = ctx.acquire('subnet', nt.get_subnet(ctx))
    interface = ctx.acquire('interface', nt.get_interface(ctx))

    image = ctx.acquire_res('image', gl.get_image(ctx))
    volume = ctx.acquire('volume', cd.get_volume(ctx))

    keypair = ctx.acquire('keypair', nv.get_keypair(ctx))
    flavor = ctx.acquire_res('flavor', nv.get_flavor(ctx))
    server = ctx.acquire('server', nv.get_server(ctx))

    floating_ip = ctx.acquire('floating_ip', nt.get_floating_ip(ctx))
    server_floating_ip = ctx.acquire('server_floating_ip', nv.get_server_floating_ip(ctx))

    sg = ctx.acquire('sg', nt.get_sg(ctx))

    print('Setup complete')

def do_tests(ctx):
    tests.test_ssh_security(ctx)

def main():
    try:
        error_stack.clear()
        with BaseContext() as ctx:
            initial_setup(ctx)
            do_tests(ctx)
    except OSCInvariantError:
        print('An invariant violation occured')
        log_error(ErrorType.TEST)
    except:
        print('An error occured during setup')
        log_error()
    if error_stack:
        slack_report(error_stack)
    else:
        print('Success!')

if __name__ == '__main__':
    main()
