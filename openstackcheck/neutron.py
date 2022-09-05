from contextlib import contextmanager

from neutronclient.v2_0 import client

@contextmanager
def get_neutron(ctx):
    with client.Client(session=ctx.auth) as neutron:
        yield neutron

@contextmanager
def get_router(ctx):
    request = {'router': {'name': 'smokecheckrouter','admin_state_up': True}}
    router = ctx.neutron.create_router(request)
    router_id = router['router']['id']

    networks = neutron.list_networks(name='public')
    network_id = networks['networks'][0]['id']
    router_dict = {'network_id': network_id}

    neutron.add_gateway_router(router_id, router_dict)

    ctx.neutron.add_gate
    yield router
    ctx.neutron.delete_router(router_id)
