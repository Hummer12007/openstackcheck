from .ctx import context, resource

from openstackcheck.config import env

flavor = env.str('NOVA_FLAVOR', None)

@context
def get_keypair(ctx):
    keypair = ctx.auth.create_keypair('ssh_key')
    print('Created keypair', keypair.id)
    yield keypair
    ctx.auth.delete_keypair(keypair.id)
    print('Deleted keypair', keypair.id)

@resource
def get_flavor(ctx):
    flavor_id = None
    if flavor:
        flavor_id = ctx.auth.get_flavor(flavor).id
    else:
        flavor_id = ctx.auth.get_flavor_by_ram(ctx.image.min_ram).id
    print('Found flavor', flavor_id)
    return flavor_id

DEFAULT_SERVER_NAME = 'smokecheckvm'

@context
def get_server(ctx):
    server = ctx.auth.create_server(DEFAULT_SERVER_NAME, boot_volume=ctx.volume.id, flavor=ctx.flavor, network=ctx.network, key_name=ctx.keypair.name)
    print('Created server', server.id)
    server = ctx.auth.compute.wait_for_server(server)
    print('Server up:', server.id)
    yield server
    ctx.auth.delete_server(server.id)
    ctx.auth.compute.wait_for_delete(server)
    print('Deleted server', server.id)

@context
def get_server_floating_ip(ctx):
    ctx.auth.compute.add_floating_ip_to_server(ctx.server, ctx.floating_ip.floating_ip_address)
    print('Assigned', ctx.floating_ip.floating_ip_address, 'to server', ctx.server.id)
    yield None
    ctx.auth.compute.remove_floating_ip_from_server(ctx.server, ctx.floating_ip.floating_ip_address)
    print('Removed', ctx.floating_ip.floating_ip_address, 'from server', ctx.server.id)

@context
def get_server_sg(ctx):
    ctx.auth.compute.add_security_group_to_server(ctx.server.id, ctx.sg)
    print('Added security group', ctx.sg.id, 'to server', ctx.server.id)
    yield None
    ctx.auth.compute.remove_security_group_from_server(ctx.server.id, ctx.sg)
    print('Removed security group', ctx.sg.id, 'from server', ctx.server.id)
