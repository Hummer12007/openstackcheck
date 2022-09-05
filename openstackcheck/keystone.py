import secrets

from contextlib import contextmanager

from keystoneclient import client
from keystoneauth1.identity import v3

import openstackcheck.config as cfg

import openstackcheck.auth as osca

@contextmanager
def get_domain(ctx):
    domain = ctx.admin.create_domain(cfg.test_domain, description='Temporary domain for smoke test')
    print('Created domain')
    yield domain
    ctx.admin.delete_domain(domain.id)
    print('Deleted domain')

@contextmanager
def get_project(ctx):
    proj = ctx.admin.create_project(cfg.test_project, ctx.domain.id, description='Temporary project for smoke test')
    print('Created project')
    yield proj
    ctx.admin.delete_project(proj.id, ctx.domain.id)
    print('Deleted project')

@contextmanager
def get_user(ctx):
    ks = ctx['ks']
    ctx.acquire_res('username', 'test_user')
    ctx.acquire_res('password', secrets.token_urlsafe(16))
    user = ctx.admin.create_user(ctx.username, password=ctx.password, domain_id=ctx.domain.id, default_project=ctx.project.id)
    yield user
    ctx.admin.delete_user(user.id, ctx.domain.id)

def get_auth(ctx):
    auth = dict(
        auth_url=osca.keystone_url,
        username=ctx.username,
        password=ctx.password,
        project_id=ctx.project_id,
        user_domain_id=ctx.domain_id,
        project_domain_id=ctx.domain_id,
    )

    return connection.Connection(auth=auth, identity_interface='public')
