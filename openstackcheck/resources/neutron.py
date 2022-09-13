from .ctx import context
from openstackcheck.config import env

neutron_external_net = env.str('NEUTRON_EXTERNAL_NET', 'public')

@context
def get_router(ctx):
    pubnet = ctx.auth.get_network(neutron_external_net)
    router = ctx.auth.create_router('smokecheckrouter', ext_gateway_net_id=pubnet.id)
    print('Created router', router.id)
    yield router
    ctx.auth.network.delete_router(router.id)
    print('Deleted router', router.id)

@context
def get_network(ctx):
    net = ctx.auth.network.create_network(name='smokechecknet')
    print('Created network', net.id)
    yield net
    ctx.auth.network.delete_network(net)
    print('Deleted network', net.id)

@context
def get_subnet(ctx):
    subnet = ctx.auth.network.create_subnet(name='smokechecksubnet', network_id=ctx.network.id, ip_version='4', cidr='10.238.0.0/24', gateway_ip='10.238.0.254')
    print('Created subnet', subnet.id)
    yield subnet
    ctx.auth.network.delete_subnet(subnet)
    print('Deleted subnet', subnet.id)

@context
def get_interface(ctx):
    ctx.auth.network.add_interface_to_router(ctx.router, ctx.subnet.id)
    print('Bound interface to router', ctx.router.id)
    yield None
    ctx.auth.network.remove_interface_from_router(ctx.router, ctx.subnet.id)
    print('Unbound interface from router', ctx.router.id)

@context
def get_floating_ip(ctx):
    ip = ctx.auth.available_floating_ip()
    print('Allocated ip', ip.floating_ip_address)
    yield ip
    ctx.auth.delete_floating_ip(ip.id)
    print('Deleted ip', ip.floating_ip_address)

@context
def get_sg(ctx):
    sg = ctx.auth.network.create_security_group(name='openstackchecksg')
    rule = ctx.auth.network.create_security_group_rule(
        security_group_id=sg.id,
        direction='ingress', remote_ip_prefix='0.0.0.0/0',
        protocol='tcp', port_range_max=22, port_range_min=22,
        ethertype='IPv4'
    )
    print('Created security group', sg.id)
    yield sg
    ctx.auth.network.delete_security_group_rule(rule)
    ctx.auth.network.delete_security_group(sg)
    print('Deleted security group', sg.id)
