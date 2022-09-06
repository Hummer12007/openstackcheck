from contextlib import contextmanager

from paramiko import RSAKey
from novaclient import client

@contextmanager
def get_nova(ctx):
    with client.Client('2', session=ctx.auth) as nova:
        yield nova

@contextmanager
def get_keypair(ctx):
    key = ctx.acquire('keypair', RSAKey.generate(4096))
    keypair = ctx.auth.create_keypair('ssh_key', public_key=key.get_base64())
    print('Created keypair', keypair.id)
    yield keypair
    ctx.auth.delete_keypair(keypair.id)
    print('Deleted keypair', keypair.id)
