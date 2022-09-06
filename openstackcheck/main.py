import traceback
import paramiko

import openstack.connection as osc

import openstack.identity.v3 as oi
import openstack.block_storage.v3 as ob
import openstack.compute.v2 as oc

import openstackcheck.nova as nv
import openstackcheck.glance as gl
import openstackcheck.keystone as ks
import openstackcheck.cinder as cd

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

    image_id: str

    volume: ob.volume.Volume

    keypair: oc.keypair.Keypair


def do_tests(ctx):
    ctx.acquire_res('admin', get_admin_auth())

    domain = ctx.acquire('domain', ks.get_domain(ctx))
    project = ctx.acquire('project', ks.get_project(ctx))
    user = ctx.acquire('user', ks.get_user(ctx))
    auth = ctx.acquire_res('auth', ks.get_auth(ctx))

    image_id = ctx.acquire_res('image_id', gl.get_image_id(ctx))

    volume = ctx.acquire('volume', cd.get_volume(ctx))
    keypair = ctx.acquire('keypair', nv.get_keypair(ctx))
    image_flavor = ctx.acquire_res('image_flavor', nv.get_image_flavor(ctx))


def main():
    with BaseContext() as ctx:
        try:
            do_tests(ctx)
        except:
            print('An error occured, cleaning up')
            print(traceback.format_exc())

if __name__ == '__main__':
    main()
