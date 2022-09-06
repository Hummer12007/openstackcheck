from contextlib import contextmanager

from openstackcheck.config import env

image_flavor = env.str('NOVA_IMAGE_FLAVOR', None)

@contextmanager
def get_keypair(ctx):
    keypair = ctx.auth.create_keypair('ssh_key')
    print('Created keypair', keypair.id)
    yield keypair
    ctx.auth.delete_keypair(keypair.id)
    print('Deleted keypair', keypair.id)

def get_image_flavor(ctx):
    flavor_id = None
    if image_flavor:
        flavor_id = ctx.auth.get_flavor(image_flavor).id
    else:
        flavor_id = ctx.auth.get_flavor_by_ram(128).id
    print('Found flavor', flavor_id)
    return flavor_id
