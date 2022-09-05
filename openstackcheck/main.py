import paramiko

from keystoneauth1.session import Session
import keystoneclient.v3 as ksc
import novaclient.v2 as nvc
import cinderclient.v3 as cdc

import openstackcheck.nova as nv
import openstackcheck.glance as gl
import openstackcheck.keystone as ks
import openstackcheck.cinder as cd

from openstackcheck.base import BaseContext

class OSCContext(BaseContext):
    ks: ksc.Client
    domain: ksc.domains.Domain
    project: ksc.projects.Project
    username: str
    password: str
    user: ksc.users.User

    auth: Session

    image_id: str

    cinder: cdc.Client
    volume: cdc.volumes_base.Volume

    nova: nvc.Client
    keypair: paramiko.RSAKey
    nova_keypair: nvc.keypairs.Keypair


def main():
    with BaseContext() as ctx:
        ctx.acquire_res('ks', ks.get_keystone())
        domain = ctx.acquire('domain', ks.get_domain(ctx))
        project = ctx.acquire('project', ks.get_project(ctx))
        user = ctx.acquire('user', ks.get_user(ctx))
        auth = ctx.acquire('auth', ks.get_auth(ctx))

        image_id = ctx.acquire_res('image_id', gl.get_image_id(ctx))
        cinder = ctx.acquire('cinder', cd.get_cinder(ctx))
        volume = ctx.acquire('volume', cd.get_volume(ctx))

        nova = ctx.acquire('nova', nv.get_nova(ctx))
        nova_keypair = ctx.acquire('nova_keypair', nv.get_keypair(ctx))
