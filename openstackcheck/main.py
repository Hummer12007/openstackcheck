import paramiko

from keystoneauth1.session import Session
import keystoneclient.v3 as ksc
import novaclient.v2 as nvc
import cinderclient.v3 as cdc

import openstack.connection as osc

import openstack.identity.v3 as oi
import openstackcheck.nova as nv
import openstackcheck.glance as gl
import openstackcheck.keystone as ks
import openstackcheck.cinder as cd

from openstackcheck.auth import get_admin_auth
from openstackcheck.base import BaseContext

class OSCContext(BaseContext):
    admin: osc.Connection

    ks: ksc.Client
    domain: oi.endpoint.Endpoint
    project: oi.project.Project
    username: str
    password: str
    user: oi.user.User

    auth: osc.Connection

    image_id: str

    cinder: cdc.Client
    volume: cdc.volumes_base.Volume

    nova: nvc.Client
    keypair: paramiko.RSAKey
    nova_keypair: nvc.keypairs.Keypair


def main():
    with BaseContext() as ctx:
        ctx.acquire_res('admin', get_admin_auth())
        domain = ctx.acquire('domain', ks.get_domain(ctx))
        project = ctx.acquire('project', ks.get_project(ctx))
        user = ctx.acquire('user', ks.get_user(ctx))
        auth = ctx.acquire_res('auth', ks.get_auth(ctx))
        return

        image_id = ctx.acquire_res('image_id', gl.get_image_id(ctx))
        cinder = ctx.acquire('cinder', cd.get_cinder(ctx))
        volume = ctx.acquire('volume', cd.get_volume(ctx))

        nova = ctx.acquire('nova', nv.get_nova(ctx))
        nova_keypair = ctx.acquire('nova_keypair', nv.get_keypair(ctx))

if __name__ == '__main__':
    main()
