import secrets

from contextlib import contextmanager

from openstack import connection

import openstackcheck.config as cfg
import openstackcheck.auth as osca

@contextmanager
def get_domain(ctx):
    domain = ctx.admin.create_domain(cfg.test_domain, description='Temporary domain for smoke test')
    print('Created domain', domain.id)
    yield domain
    ctx.admin.delete_domain(domain.id)
    print('Deleted domain', domain.id)

@contextmanager
def get_project(ctx):
    proj = ctx.admin.create_project(cfg.test_project, ctx.domain.id, description='Temporary project for smoke test')
    print('Created project', proj.id)
    yield proj
    ctx.admin.delete_project(proj.id, ctx.domain.id)
    print('Deleted project', proj.id)

@contextmanager
def get_user(ctx):
    ctx.acquire_res('username', 'test_user')
    ctx.acquire_res('password', secrets.token_urlsafe(16))
    user = ctx.admin.create_user(ctx.username, password=ctx.password, domain_id=ctx.domain.id, default_project=ctx.project.id)
    print('Created user', user.id)
    ctx.admin.grant_role('admin', user=user.id, project=ctx.project.id, domain=ctx.domain.id, wait=True)
    print('Granted role admin on', ctx.project.id, 'to', user.id)
    yield user
    ctx.admin.delete_user(user.id)
    print('Deleted user', user.id)

def get_auth(ctx):
    auth = dict(
        auth_url=osca.keystone_url,
        username=ctx.username,
        password=ctx.password,
        project_id=ctx.project.id,
        user_domain_id=ctx.domain.id,
        project_domain_id=ctx.domain.id,
    )

    con = connection.Connection(auth=auth, identity_interface='public')

    return con
